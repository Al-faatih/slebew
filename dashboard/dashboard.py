import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

st.set_page_config(page_title="E-Commerce Dashboard", layout="wide")

# ======================
# LOAD DATA (FIX PATH)
# ======================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

orders = pd.read_csv(os.path.join(BASE_DIR, 'data/orders_dataset.csv'))
order_items = pd.read_csv(os.path.join(BASE_DIR, 'data/order_items_dataset.csv'))
products = pd.read_csv(os.path.join(BASE_DIR, 'data/products_dataset.csv'))
product_category = pd.read_csv(os.path.join(BASE_DIR, 'data/product_category_name_translation.csv'))
customers = pd.read_csv(os.path.join(BASE_DIR, 'data/customers_dataset.csv'))
payments = pd.read_csv(os.path.join(BASE_DIR, 'data/order_payments_dataset.csv'))
reviews = pd.read_csv(os.path.join(BASE_DIR, 'data/order_reviews_dataset.csv'))

# ======================
# CLEANING
# ======================
orders['order_purchase_timestamp'] = pd.to_datetime(orders['order_purchase_timestamp'])

# ======================
# SIDEBAR
# ======================
st.sidebar.title("Dashboard Menu")
menu = st.sidebar.selectbox("Pilih Analisis", [
    "Overview",
    "Metode Pembayaran",
    "Top Seller",
    "Trend Order"
])

# ======================
# OVERVIEW
# ======================
if menu == "Overview":
    st.title("📊 E-Commerce Dashboard")
    st.write("Analisis data e-commerce 2017–2018")

    st.metric("Total Orders", len(orders))
    st.metric("Total Items", len(order_items))
    st.metric("Total Customers", len(customers))

# ======================
# PAYMENT ANALYSIS
# ======================
elif menu == "Metode Pembayaran":
    st.title("💳 Metode Pembayaran")

    df_pay = orders.merge(payments, on='order_id')

    fig, ax = plt.subplots()
    df_pay['payment_type'].value_counts().plot(kind='bar', ax=ax)
    st.pyplot(fig)

# ======================
# TOP SELLER
# ======================
elif menu == "Top Seller":
    st.title("🏆 Top Seller")

    top_seller = order_items['seller_id'].value_counts().head(10)

    fig, ax = plt.subplots()
    top_seller.plot(kind='barh', ax=ax)
    st.pyplot(fig)

# ======================
# TREND ORDER
# ======================
elif menu == "Trend Order":
    st.title("📈 Trend Order")

    orders['month'] = orders['order_purchase_timestamp'].dt.to_period('M')
    monthly = orders.groupby('month')['order_id'].count()

    fig, ax = plt.subplots()
    monthly.plot(ax=ax)
    st.pyplot(fig)
