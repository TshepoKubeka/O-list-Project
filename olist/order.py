import pandas as pd
import numpy as np
from olist.utils import haversine_distance
from olist.data import Olist


class Order:
    '''
    DataFrames containing all orders as index,
    and various properties of these orders as columns
    '''

    def __init__(self):
        # Assign an attribute ".data" to all new instances of Order
        self.data = Olist().get_data()

    def get_wait_time(self, is_delivered=True):
        """
        Returns a DataFrame with:
        [order_id, wait_time, expected_wait_time, delay_vs_expected, order_status]
        and filters out non-delivered orders unless specified
        """
        # Hint: Within this instance method, you have access to the instance of the class Order in the variable self, as well as all its attributes
        orders = self.data['orders'].copy()
        if is_delivered:
            orders = orders[orders['order_status'] == 'delivered']
        # Handle `datetime`
        orders['order_purchase_timestamp'] = pd.to_datetime(orders['order_purchase_timestamp'])
        orders['order_approved_at'] = pd.to_datetime(orders['order_approved_at'])
        orders['order_delivered_carrier_date'] = pd.to_datetime(
            orders['order_delivered_carrier_date'])
        orders['order_delivered_customer_date'] = pd.to_datetime(
            orders['order_delivered_customer_date'])
        orders['order_estimated_delivery_date'] = pd.to_datetime(
            orders['order_estimated_delivery_date'])
        # Compute `wait_time`
        orders['wait_time'] = (orders['order_delivered_customer_date'] - orders[
            'order_purchase_timestamp']).dt.days
        # Compute `expected_wait_time`
        orders['expected_wait_time'] = (orders['order_estimated_delivery_date'] - orders[
            'order_purchase_timestamp']).dt.days
        # Compute `delay_vs_expected`
        orders['delay_vs_expected'] = orders['wait_time'] - orders['expected_wait_time']
        orders.loc[orders["delay_vs_expected"] < 0, "delay_vs_expected"] = 0
        return orders[
            ['order_id', 'wait_time', 'expected_wait_time', 'delay_vs_expected', 'order_status']]

    def get_review_score(self):
        """
        Returns a DataFrame with:
        order_id, dim_is_five_star, dim_is_one_star, review_score
        """
        reviews = self.data['order_reviews'].copy()
        # dim_is_five_star
        reviews['dim_is_five_star'] = np.where(reviews['review_score'] == 5, 1, 0)
        # dim_is_one_star
        reviews['dim_is_one_star'] = np.where(reviews['review_score'] == 1, 1, 0)
        return reviews[
            ['order_id', 'dim_is_five_star', 'dim_is_one_star', 'review_score']]

    def get_number_products(self):
        """
        Returns a DataFrame with:
        order_id, number_of_products
        """
        number_products = self.data['order_items'].copy()
        _df = number_products['order_id'].value_counts().to_frame().reset_index()
        _df.columns = ['order_id', 'number_of_products']
        return _df

    def get_number_sellers(self):
        """
        Returns a DataFrame with:
        order_id, number_of_sellers
        """
        number_sellers = self.data['order_items'].copy()
        _df = number_sellers.groupby('order_id')[
            'seller_id'].nunique().to_frame().reset_index()
        _df.columns = ['order_id', 'number_of_sellers']
        return _df

    def get_price_and_freight(self):
        """
        Returns a DataFrame with:
        order_id, price, freight_value
        """
        price_and_freight = self.data['order_items'][['order_id', 'price', 'freight_value']].copy()
        _df = price_and_freight.groupby('order_id').agg('sum').reset_index()
        return _df

    # Optional
    def get_distance_seller_customer(self):
        """
        Returns a DataFrame with:
        order_id, distance_seller_customer
        """
        # getting all the primary keys

        order_customer = self.data['orders'].copy()
        order_customer_seller = order_customer.merge(self.data['order_items'], on='order_id')[
            ['order_id', 'customer_id', 'seller_id']]
        order_customer_seller.drop_duplicates(inplace=True)

        order_customer_seller = order_customer_seller.merge(self.data['customers'], on='customer_id') \
            [['order_id', 'customer_id', 'customer_zip_code_prefix', 'seller_id']]

        order_customer_seller = order_customer_seller.merge(self.data['sellers'], on='seller_id') \
            [['order_id', 'customer_id', 'customer_zip_code_prefix', 'seller_id',
              'seller_zip_code_prefix']]

        # dealing with the geolocation table

        geo = self.data['geolocation'].copy()
        geo = geo.groupby('geolocation_zip_code_prefix')[['geolocation_lat', 'geolocation_lng']].mean()
        geo.columns = ['lat', 'long']

        # merging our two tables twice (once for sellers, once for customers)

        order_customer_seller = order_customer_seller.merge(geo, left_on='customer_zip_code_prefix',
                                                            right_on=geo.index) \
            .rename({'lat': 'customer_lat', 'long': 'customer_long'}, axis='columns') \
            .merge(geo, left_on='seller_zip_code_prefix', right_on=geo.index) \
            .rename({'lat': 'seller_lat', 'long': 'seller_long'}, axis='columns')

        # computing the haversine distance

        order_customer_seller['distance_seller_customer'] = order_customer_seller \
            .apply(lambda row: haversine_distance(row['customer_long'], row['customer_lat'],
                                                  row['seller_long'], row['seller_lat']), axis=1)

        # taking the average per order and deleting other columns

        return order_customer_seller[['order_id', 'distance_seller_customer']] \
            .groupby('order_id').mean().reset_index()

    def get_training_data(self,
                          is_delivered=True,
                          with_distance_seller_customer=False):
        """
        Returns a clean DataFrame (without NaN), with the all following columns:
        ['order_id', 'wait_time', 'expected_wait_time', 'delay_vs_expected',
        'order_status', 'dim_is_five_star', 'dim_is_one_star', 'review_score',
        'number_of_products', 'number_of_sellers', 'price', 'freight_value',
        'distance_seller_customer']
        """
        # Hint: make sure to re-use your instance methods defined above
        final_df = self.get_wait_time(is_delivered=is_delivered)
        final_df = final_df.merge(self.get_review_score(), how='inner', on='order_id')
        final_df = final_df.merge(self.get_number_products(), how='inner', on='order_id')
        final_df = final_df.merge(self.get_number_sellers(), how='inner', on='order_id')
        final_df = final_df.merge(self.get_price_and_freight(), how='inner', on='order_id')
        if with_distance_seller_customer:
            final_df = final_df.merge(self.get_distance_seller_customer(), how='inner', on='order_id')
        final_df.dropna(inplace=True)
        return final_df
