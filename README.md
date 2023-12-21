# RFM Analysis-FLO RFM Analysis
![rfm-analizi](https://github.com/ymetinyilmazoglu/RFM-Analysis/assets/136450475/062cd5f2-6f41-4108-9031-ebbba3934a26)
-What is RFM Analysis?
RFM Analysis is a technique used for customer segmentation. It allows customers to be divided into groups based on their purchasing habits and to develop strategies specific to groups. It is based on 3 basic metrics that start with 3 letters in the name RFM analysis.   First, let's look at what these three concepts are.
**_Recency_**
It is calculated based on the dates of the customer's purchases. It is the number of days between the customer's last shopping date and our analysis date or the date we base it on.
**_Frequency_**
It is the number of purchases made by the customer within the date range specified for analysis. In this metric, if the number of customers who shop only once is higher than the total customers, there will be an asymmetric distribution, so customers who make one-time purchases can be evaluated separately for a more accurate analysis.
**_Monatery_**
It is the total monetary value of the purchases made within the date range recorded for analysis.

-Business Problem
FLO, an online shoe store, wants to divide its customers into segments and determine marketing strategies according to these segments. For this purpose, the behavior of the customers will be defined and groups will be created according to these behavioral clusters.
-Features of Dataset
* Total Row : 19.945
* Total Features : 12
* CSV File Size : 2.7 MB
-The Story Of The Dataset
The data set includes OmniChannel (both online and offline shoppers) who made their last purchases from Flo in 2020 - 2021.It consists of information obtained from the past shopping behavior of customers.
* master_id: Unique customer number
* order_channel: Which channel of the shopping platform used (Android, iOS, desktop, mobile)
* last_order_channel: Channel where the last shopping was made
* first_order_date: Customer's first shopping date
* last_order_date: Customer's latest shopping date
* last_order_date_online: Customer's latest shopping date on the online platform
* last_order_date_offline: Customer's latest shopping date on offline platform
* order_num_total_ever_online: Customer's total number of shopping on the online platform
* order_num_total_ever_offline: Customer's total number of shopping on the offline platform
* customer_value_total_ever_offline: Total fee paid by the customer in offline shopping
* customer_value_total_ever_online: Total fee paid by the customer in online shopping
* interested_in_categories_12: List of categories where the customer shopping in the last 12 months

-Customer Segments
![RFM-Segmentleri](https://github.com/ymetinyilmazoglu/RFM-Analysis/assets/136450475/3aaac67b-016f-472a-a265-c102d31d1613)


