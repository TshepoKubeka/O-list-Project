Welcome to my Decision Science project 🎉

We will analyze a dataset provided by e-commerce marketplace [Olist](https://www.olist.com).

## Olist Data

The Olist dataset consists of information (customers, reviews, products etc..) on 100k orders on [Olist Store](http://www.olist.com/).
The Olist dataset consists of information (customers, reviews, products etc..) on 100k orders from the [Olist Store](http://www.olist.com/).

9 csvs (~120mb) are available and can be [downloaded here](https://www.kaggle.com/olistbr/brazilian-ecommerce). We recommend placing them in the `data/csv` folder.

9 csv (~120mb) are available and can be [downloaded here](https://www.kaggle.com/olistbr/brazilian-ecommerce). We recommend placing them under the `data/csv` folder.
- <a href="#data_model">**Data Model**</a>
- <a href="#olist_customers_dataset">**olist_customers_dataset**</a>
- <a href="#olist_geolocation_dataset">**olist_geolocation_dataset**</a>
The schema below represents each dataset and which key to use to join them:

### olist_customers_dataset

This dataset has information about the customer and its location. Use it to identify unique customers in the orders dataset and to find the orders delivery location.
This dataset has information about the customer and their location. Use it to identify unique customers in the orders dataset and to find the orders delivery location.

- `customer_id`: key to the orders dataset. Each order has a unique customer_id.
- `customer_unique_id`: unique identifier of a customer.
This dataset has information about the customer and its location. Use it to iden

### olist_geolocation_dataset

This dataset has information Brazilian zip codes and its lat/lng coordinates. Use it to plot maps and find distances between sellers and customers.
This dataset has information about Brazilian zip codes and lat/lng coordinates. Use it to plot maps and find distances between sellers and customers.

- `geolocation_zip_code_prefix`: first 5 digits of zip code
- `geolocation_lat`: latitude
This dataset has information Brazilian zip codes and its lat/lng coordinates. Us

This dataset includes data about the items purchased within each order.

⚠️ If 3 items are purchased in an order, the dataset will display one row per item. If the same product is bought 2 times, 2 rows will be displayed.
⚠️ If 3 items are purchased in an order, the dataset will display one row per item. If the same product is bought twice, 2 rows will be displayed.

- `order_id`: order unique identifier
- `order_item_id`: sequential number identifying number of items included in the same order.
- `product_id`: product unique identifier
- `seller_id`: seller unique identifier
- `shipping_limit_date`: Shows the seller shipping limit date for handling the order over to the logistic partner.
- `shipping_limit_date`: shows the seller shipping limit date for handling the order over to the logistic partner.
- `price`: item price
- `freight_value`: item freight value item (if an order has more than one item the freight value is splitted between items)
- `freight_value`: item freight value (if an order has more than one item the freight value is split between items)

<div id="olist_order_payments_dataset">

### olist_order_payments_dataset

This dataset includes data about the orders payment options.
This dataset includes data about order payment options.

- `order_id`: unique identifier of an order.
- `payment_sequential`: a customer may pay an order with more than one payment method. If he does so, a sequence will be created to accommodate all payments.
- `payment_sequential`: a customer may pay for an order with more than one payment method. If they do, a sequence will be created to accommodate all payments.
- `payment_type`: method of payment chosen by the customer.
- `payment_installments`: number of installments chosen by the customer.
- `payment_value`: transaction value.
This dataset includes data about the orders payment options.

### olist_order_reviews_dataset

This dataset includes data about the reviews made by the customers.
This dataset includes data about the reviews made by a customer.

After a customer purchases the product from Olist Store a seller gets notified to fulfill that order. Once the customer receives the product, or the estimated delivery date is due, the customer gets a satisfaction survey by email where he can give a note for the purchase experience and write down some comments.
After a customer purchases the product from the Olist Store, a seller gets notified to fulfill that order. Once the customer receives the product, or the estimated delivery date is due, the customer gets a satisfaction survey by email where they can leave a note for the purchase experience and write some comments.

- `review_id`: unique review identifier
- `order_id`: unique order identifier
- `review_score`: Note ranging from 1 to 5 given by the customer on a satisfaction survey.
- `review_comment_title`: Comment title from the review left by the customer, in Portuguese.
- `review_comment_message`: Comment message from the review left by the customer, in Portuguese.
- `review_creation_date`: Shows the date in which the satisfaction survey was sent to the customer.
- `review_answer_timestamp`: Shows satisfaction survey answer timestamp.
- `review_score`: score ranging from 1 to 5 given by the customer on a satisfaction survey.
- `review_comment_title`: title from the review left by the customer, in Portuguese.
- `review_comment_message`: message from the review left by the customer, in Portuguese.
- `review_creation_date`: shows the date in which the satisfaction survey was sent to the customer.
- `review_answer_timestamp`: shows the satisfaction survey response timestamp.

<div id="olist_orders_dataset">

### olist_orders_dataset

This is the core dataset. From each order you might find all other information.
This is the core dataset. For each order, you can find all other information.

- `order_id`: unique identifier of the order.
- `customer_id`: key to the customer dataset. Each order has a unique customer_id.
- `order_status`: Reference to the order status (delivered, shipped, etc).
- `order_purchase_timestamp`: Shows the purchase timestamp.
- `order_approved_at`: Shows the payment approval timestamp.
- `order_delivered_carrier_date`: Shows the order posting timestamp. When it was handled to the logistic partner.
- `order_delivered_customer_date`: Shows the actual order delivery date to the customer.
- `order_estimated_delivery_date`: Shows the estimated delivery date that was informed to customer at the purchase moment.
- `order_status`: reference to the order status (delivered, shipped, etc).
- `order_purchase_timestamp`: shows the purchase timestamp.
- `order_approved_at`: shows the payment approval timestamp.
- `order_delivered_carrier_date`: shows the order posting timestamp, i.e. when it was handed to the logistic partner.
- `order_delivered_customer_date`: shows the actual order delivery date to the customer.
- `order_estimated_delivery_date`: shows the estimated delivery date that was informed to the customer at the time of purchase.

<div id="olist_products_dataset">

This dataset includes data about the sellers that fulfilled orders made at Olist

### product_category_name_translation

Translates the product_category_name to english.
Translates the product_category_name to English.

- `product_category_name`: category name in Portuguese
- `product_category_name_english`: category name in English
