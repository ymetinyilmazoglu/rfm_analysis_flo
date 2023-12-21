
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
###############################################################

df_first = pd.read_csv("flo_data_20k.csv")
df = df_first.copy()

###############################################################
# TASK 2: Examine the first 10 rows of the data set, 
# variable names, size, descriptive statistics,
# null values, and variable types.
###############################################################
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


###############################################################
# TASK 3: Omnichannel means that customers shop from both online and offline platforms.
# Create new variables for each customer's total number of purchases and spending.
################################################################

# total order of omnichannel (offline + online), total number of orders
df["Total_order"]=df["order_num_total_ever_online"]+df["order_num_total_ever_offline"]
# total spend of omnichannel (offline + online), total expenditure
df["Total_value"] = df["customer_value_total_ever_offline"]+df["customer_value_total_ever_online"]

df.head()

###############################################################
# TASK 4: Examine the types of variables. Convert the object variables containing date in the data set to date format.
################################################################
for i in df.columns:
    if "date" in i:
        df[i] = df[i].apply(pd.to_datetime)

# df["last_order_date"] = df["last_order_date"].apply(pd.to_datetime)



# 5. Alışveriş kanallarındaki müşteri sayısının, toplam alınan ürün sayısı ve toplam harcamaların dağılımına bakınız. 

df.groupby('master_id').agg({'Total_order':["count","mean"],
                                 "Total_value":["count","mean"]})


# 6. En fazla kazancı getiren ilk 10 müşteriyi sıralayınız.

df.groupby('master_id').agg({'Total_value': 'sum'}).sort_values("Total_value", ascending=False).head(10)



# 7. En fazla siparişi veren ilk 10 müşteriyi sıralayınız.

df.groupby('master_id').agg({'Total_order': 'sum'}).sort_values("Total_order", ascending=False).head(10)



# 8. Veri ön hazırlık sürecini fonksiyonlaştırınız.


def rfm_olusturma(dataframe, csv=False):
    import datetime as dt
    import pandas as pd
    # Veriyi Hazırlama
    if csv:
        df = pd.read_csv(dataframe)
    else:
        df = dataframe.copy()
    pd.set_option('display.max_columns', None)
    pd.set_option('display.float_format', lambda x: '%.2f' % x)


    df["Total_order"] = df["order_num_total_ever_online"] + df["order_num_total_ever_offline"]
    df["Total_value"] = df["customer_value_total_ever_offline"] + df["customer_value_total_ever_online"]

    df['first_order_date'] = pd.to_datetime(df['first_order_date'])
    df['last_order_date'] = pd.to_datetime(df['last_order_date'])
    df['last_order_date_online'] = pd.to_datetime(df['last_order_date_online'])
    df['last_order_date_offline'] = pd.to_datetime(df['last_order_date_offline'])

    return df
df = rfm_olusturma(df, csv=False)

###############################################################
# GÖREV 2: RFM Metriklerinin Hesaplanması
###############################################################

# Veri setindeki en son alışverişin yapıldığı tarihten 2 gün sonrasını analiz tarihi
df["last_order_date"].max()

today_date = dt.datetime(2021, 6 ,1)
type(today_date)

rfm = df.groupby('master_id').agg({
    "last_order_date": lambda last_order_date: (today_date - last_order_date.max()).days,
    "Total_order": lambda Total_order: Total_order.sum(),
    "Total_value": lambda Total_value: Total_value.sum()})

rfm.columns = ['recency', 'frequency', 'monetary']
rfm.describe().T

# customer_id, recency, frequnecy ve monetary değerlerinin yer aldığı yeni bir rfm dataframe


###############################################################
# GÖREV 3: RF ve RFM Skorlarının Hesaplanması (Calculating RF and RFM Scores)
###############################################################

#  Recency, Frequency ve Monetary metriklerini qcut yardımı ile 1-5 arasında skorlara çevrilmesi ve
# Bu skorları recency_score, frequency_score ve monetary_score olarak kaydedilmesi
rfm["recency_score"] = pd.qcut(rfm['recency'], 5, labels=[5, 4, 3, 2, 1])
rfm["frequency_score"] = pd.qcut(rfm['frequency'].rank(method="first"), 5, labels=[1, 2, 3, 4, 5])
rfm["monetary_score"] = pd.qcut(rfm['monetary'], 5, labels=[1, 2, 3, 4, 5])

# recency_score ve frequency_score’u tek bir değişken olarak ifade edilmesi ve RF_SCORE olarak kaydedilmesi
rfm["RFM_SCORE"] = (rfm['recency_score'].astype(str) +
                    rfm['frequency_score'].astype(str))

###############################################################
# GÖREV 4: RF Skorlarının Segment Olarak Tanımlanması
###############################################################
# Oluşturulan RFM skorların daha açıklanabilir olması için segment tanımlama ve
# tanımlanan seg_map yardımı ile RF_SCORE'u segmentlere çevirme
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
rfm['segment'] = rfm['RFM_SCORE'].replace(seg_map,regex = True)
rfm[rfm["segment"] == "champions"]
rfm[rfm["segment"] == "cant_loose"].index
rfm.to_csv("rfmmm.csv")

###############################################################
# GÖREV 5: Aksiyon zamanı!
###############################################################

# 1. Segmentlerin recency, frequnecy ve monetary ortalamalarını inceleyiniz.


rfm[["segment", "recency", "frequency", "monetary"]].groupby("segment").agg(["mean", "count"])

# 2. RFM analizi yardımı ile 2 case için ilgili profildeki müşterileri bulunuz ve müşteri id'lerini csv ye kaydediniz.
new_df = pd.DataFrame()
new_df["champions"] = rfm[rfm["segment"] == "champions"].index
new_df["at_Risk"] = rfm[rfm["segment"] == "at_Risk"].index

new_df.to_csv("new_customers.csv")
# a. FLO bünyesine yeni bir kadın ayakkabı markası dahil ediyor. Dahil ettiği markanın ürün fiyatları genel müşteri tercihlerinin üstünde. Bu nedenle markanın
# tanıtımı ve ürün satışları için ilgilenecek profildeki müşterilerle özel olarak iletişime geçeilmek isteniliyor. Bu müşterilerin sadık  ve
# kadın kategorisinden alışveriş yapan kişiler olması planlandı. Müşterilerin id numaralarını csv dosyasına yeni_marka_hedef_müşteri_id.cvs
# olarak kaydediniz.
rfm = df

first_df = rfm["master_id","segment","interested_in_categories_12","monetary"]

# b. Erkek ve Çoçuk ürünlerinde %40'a yakın indirim planlanmaktadır. Bu indirimle ilgili kategorilerle ilgilenen geçmişte iyi müşterilerden olan ama uzun süredir
# alışveriş yapmayan ve yeni gelen müşteriler özel olarak hedef alınmak isteniliyor. Uygun profildeki müşterilerin id'lerini csv dosyasına indirim_hedef_müşteri_ids.csv
# olarak kaydediniz.




# GÖREV 6: Tüm süreci fonksiyonlaştırınız.
