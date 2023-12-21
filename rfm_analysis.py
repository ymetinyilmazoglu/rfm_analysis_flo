
###############################################################
# Customer Segmentation with RFM
###############################################################

###############################################################
# Business Problem
###############################################################
# FLO wants to segment its customers and determine marketing strategies according to these segments.
# For this, the behavior of the customers will be defined and groups will be formed according to these behavior clusters.

###############################################################
# Dataset Story
###############################################################

# The dataset consists of information obtained from the past shopping behaviors of customers who made their last
# purchases as OmniChannel (both online and offline shopper) in 2020 - 2021.

# master_id: Unique client number
# order_channel : Which channel of the shopping platform is used (Android, ios, Desktop, Mobile, Offline)
# last_order_channel : The channel where the last purchase was made
# first_order_date : The date of the customer's first purchase
# last_order_date : The date of the last purchase made by the customer
# last_order_date_online : The date of the last purchase made by the customer on the online platform
# last_order_date_offline : The date of the last purchase made by the customer on the offline platform
# order_num_total_ever_online : The total number of purchases made by the customer on the online platform
# order_num_total_ever_offline : Total number of purchases made by the customer offline
# customer_value_total_ever_offline : The total price paid by the customer for offline purchases
# customer_value_total_ever_online : The total price paid by the customer for their online shopping
# interested_in_categories_12 : List of categories the customer has purchased from in the last 12 months


###############################################################
# TASK 1: Prepare and Understand Data (Data Understanding)
###############################################################

import datetime as dt
import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.float_format', lambda x: '%.3f' % x)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.width', 500)


df_first = pd.read_csv("flo_data_20k.csv")
df = df_first.copy()


# TASK 2: Examine the first 10 rows of the data set, 
# variable names, size, descriptive statistics,
# null values, and variable types.

def check_dataframe(df, head=10):
    print("##################### Shape #####################")
    print(df.shape)
    print("##################### Info  #####################")
    print(df.info())
    print("##################### Types #####################")
    print(df.dtypes)
    print("##################### Head  #####################")
    print(df.head(head))
    print("##################### Tail  ######################")
    print(df.tail(head))
    print("#################### Summary Statistics of The Dataset #####################")
    print(df.describe())
    print("###################### NA(Null Values In The Dataset) ######################")
    print(df.isnull().sum())

check_dataframe(df)



# TASK 3: Omnichannel means that customers shop from both online and offline platforms.
# Create new variables for each customer's total number of purchases and spending.


# total order of omnichannel (offline + online), total number of orders
df["Total_order"]=df["order_num_total_ever_online"]+df["order_num_total_ever_offline"]
# total spend of omnichannel (offline + online), total expenditure
df["Total_value"] = df["customer_value_total_ever_offline"]+df["customer_value_total_ever_online"]

df.head()


# TASK 4: Examine the types of variables. Convert the object variables containing date in the data set to date format.

for i in df.columns:
    if "date" in i:
        df[i] = df[i].apply(pd.to_datetime)

df["last_order_date"] = df["last_order_date"].apply(pd.to_datetime)
#2nd method solution
date_columns = df.columns[df.columns.str.contains("date")]
df[date_columns] = df[date_columns].apply(pd.to_datetime)
df.info()

# TASK 5: Look at the distribution of the number of customers in the shopping channels, the total number of products
# purchased and total expenditures.
# master_id count shows us how many purchases there are.

df.groupby("order_channel").agg({"master_id":"count",
                                "Total_order":"sum",
                                "Total_value":"sum"})



# TASK 6: Rank the top 10 customers who spend the most.


df.sort_values("Total_value", ascending=False)[:10]



# TASK 7: Rank the top 10 customers with the most purchases.


df.sort_values("Total_order", ascending=False)[:10]


# TASK 8: Functionalize the data provisioning process.

def data_processing(dataframe):
    dataframe["Total_order"] = dataframe["order_num_total_ever_online"] + dataframe["order_num_total_ever_offline"]
    dataframe["Total_value"] = dataframe["customer_value_total_ever_offline"] + dataframe["customer_value_total_ever_online"]
    date_columns = dataframe.columns[dataframe.columns.str.contains("date")]
    dataframe[date_columns] = dataframe[date_columns].apply(pd.to_datetime)
    
    return df

data_processing(df)

###############################################################
# TASK 2: Calculating RFM Metrics
###############################################################

# The analysis date is 2 days after the date of the last purchase in the data set.
df["last_order_date"].max() # 2021-05-30
analysis_date = dt.datetime(2021,6,1)
# A new rfm dataframe containing customer_id, recency, frequency and monetary values
rfm = pd.DataFrame()
rfm["customer_id"] = df["master_id"]
rfm["recency"] = (analysis_date - df["last_order_date"]).astype('timedelta64[D]')
rfm["frequency"] = df["Total_order"]
rfm["monetary"] = df["Total_value"]

rfm.head()
###############################################################
# TASK 3: Calculating RF and RFM Scores
###############################################################
# Converting Recency, Frequency and Monetary metrics into scores between 1-5 with the help of qcut and
# Saving these scores as recency_score, frequency_score and monetary_score
rfm["recency_score"] = pd.qcut(rfm['recency'], 5, labels=[5, 4, 3, 2, 1])

rfm["frequency_score"] = pd.qcut(rfm['frequency'].rank(method="first"), 5, labels=[1, 2, 3, 4, 5])

rfm["monetary_score"] = pd.qcut(rfm['monetary'], 5, labels=[1, 2, 3, 4, 5])

rfm.head()


# Expressing recency_score and frequency_score as a single variable and saving it as RF_SCORE
rfm["RF_SCORE"] = (rfm['recency_score'].astype(str) + rfm['frequency_score'].astype(str))

# Expressing recency_score and frequency_score and monetary_score as a single variable and saving it as RFM_SCORE
rfm["RFM_SCORE"] = (rfm['recency_score'].astype(str) + rfm['frequency_score'].astype(str) + rfm['monetary_score'].astype(str))

rfm.head()
###############################################################
# TASK 4: Defining RF Scores as Segments
###############################################################
# Segment definition and converting RF_SCORE to segments with the help of defined seg_map so that the
# generated RFM scores can be explained more clearly.

seg_map = {
    r'[1-2][1-2]': 'hibernating',
    r'[1-2][3-4]': 'at_Risk',
    r'[1-2]5': 'cant_loose',
    r'3[1-2]': 'about_to_sleep',
    r'33': 'need_attention',
    r'[3-4][4-5]': 'loyal_customers',
    r'41': 'promising',
    r'51': 'new_customers',
    r'[4-5][2-3]': 'potential_loyalists',
    r'5[4-5]': 'champions'
}

seg_map

rfm['segment'] = rfm['RF_SCORE'].replace(seg_map, regex=True)

rfm.head()


###############################################################
# TASK 5: Time for action!
###############################################################

# Step 1.Examine the recency, frequency and monetary averages of the segments

rfm[["segment", "recency", "frequency", "monetary"]].groupby("segment").agg(["mean", "count"])

# Step 2: With the help of RFM analysis, find the customers in the relevant profile for 2 cases and save
# the customer IDs to the csv.

# a. FLO includes a new women's shoe brand. The product prices of the brand it includes are above the general
# customer preferences. For this reason, customers in the profile who will be interested in the promotion of the
# brand and product sales are requested to be contacted privately. These customers were planned to be loyal and female
# shoppers. Save the id numbers of the customers to the csv file as new_brand_target_customer_id.cvs.

new_df = df.merge(rfm, on="master_id")

new_df = new_df[new_df["segment"].isin(["loyal_customers", "champions"])]

new_df.head()

new_df = new_df[new_df["interested_in_categories_12"].str.contains("KADIN")]

new_df.reset_index(drop=True, inplace=True)

new_df['segment'].unique()
new_df['interested_in_categories_12'].unique()

new_df["master_id"].to_csv("yeni_marka_hedef_musteri_id.csv")

# b. Up to 40% discount is planned for Men's and Children's products. We want to specifically target customers who
# are good customers in the past who are interested in categories related to this discount, but have not shopped for
# a long time and new customers. Save the ids of the customers in the appropriate profile to the csv file as
# discount_target_customer_ids.csv.

new_df2 = df.merge(rfm, on="master_id")

new_df2 = new_df2[new_df2["segment"].isin(["about_to_sleep", "new_customers"])]

new_df2.reset_index(drop=True, inplace=True)

new_df2["master_id"].to_csv("indirim_hedef_musteri_ids.csv")


