import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

st.set_page_config(page_title="E-Commerce Dashboard", layout="wide")

# ======================

# ======================
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_DIR = os.path.join(BASE_DIR, "data")

# ======================
# FUNCTION LOAD DATA 
# ======================
def load_data(filename):
    path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(path):
        st.error(f" File tidak ditemukan: {filename}")
        st.stop()
    return pd.read_csv(path)

# ======================
# LOAD DATA
# ======================
orders = load_data("orders_dataset.csv")
order_items = load_data("order_items_dataset.csv")
products = load_data("products_dataset.csv")
product_category = load_data("product_category_name_translation.csv")
customers = load_data("customers_dataset.csv")
payments = load_data("order_payments_dataset.csv")
reviews = load_data("order_reviews_dataset.csv")

# ======================
# CLEANING
# ======================
orders['order_purchase_timestamp'] = pd.to_datetime(
    orders['order_purchase_timestamp'], errors='coerce'
)

# ======================
# SIDEBAR
# ======================
st.sidebar.title(" Dashboard Menu")
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
    st.title(" E-Commerce Dashboard")
    st.write("Analisis data e-commerce 2017–2018")

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Orders", len(orders))
    col2.metric("Total Items", len(order_items))
    col3.metric("Total Customers", len(customers))

# ======================
# PAYMENT ANALYSIS
# ======================
elif menu == "Metode Pembayaran":
    st.title(" Metode Pembayaran")

    df_pay = orders.merge(payments, on='order_id', how='inner')

    payment_count = df_pay['payment_type'].value_counts()

    fig, ax = plt.subplots()
    payment_count.plot(kind='bar', ax=ax)
    ax.set_title("Distribusi Metode Pembayaran")

    st.pyplot(fig)
    st.info(f"Metode dominan: {payment_count.idxmax()}")

# ======================
# TOP SELLER
# ======================
elif menu == "Top Seller":
    st.title(" Top Seller")

    top_seller = order_items['seller_id'].value_counts().head(10)

    fig, ax = plt.subplots()
    top_seller.plot(kind='barh', ax=ax)
    ax.set_title("Top 10 Seller")

    st.pyplot(fig)

# ======================
# TREND ORDER
# ======================
elif menu == "Trend Order":
    st.title("📈 Trend Order")

    orders['month'] = orders['order_purchase_timestamp'].dt.to_period('M').astype(str)
    monthly = orders.groupby('month')['order_id'].count()

    fig, ax = plt.subplots()
    monthly.plot(ax=ax)
    ax.set_title("Trend Order per Bulan")

    st.pyplot(fig)
