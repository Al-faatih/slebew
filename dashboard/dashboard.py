import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

# ======================
# CONFIG
# ======================
st.set_page_config(page_title="E-Commerce Dashboard", layout="wide")

# ======================
# SAFE PATH LOADER
# ======================
BASE_DIR = os.path.dirname(__file__)

def load_data(file):
    path = os.path.join(BASE_DIR, "data", file)
    return pd.read_csv(path)

# ======================
# LOAD DATA
# ======================
orders = load_data("orders_dataset.csv")
order_items = load_data("order_items_dataset.csv")
products = load_data("products_dataset.csv")
payments = load_data("order_payments_dataset.csv")

# ======================
# PREPROCESSING
# ======================
orders['order_purchase_timestamp'] = pd.to_datetime(orders['order_purchase_timestamp'], errors='coerce')

# ======================
# MERGE DATA
# ======================
payments = payments.groupby("order_id", as_index=False)["payment_value"].sum()

df = orders.merge(order_items, on="order_id", how="inner")
df = df.merge(products, on="product_id", how="inner")
df = df.merge(payments, on="order_id", how="inner")

# ======================
# FILTER
# ======================
st.sidebar.header("Filter Waktu")

min_date = df['order_purchase_timestamp'].min()
max_date = df['order_purchase_timestamp'].max()

start = st.sidebar.date_input("Start", min_date)
end = st.sidebar.date_input("End", max_date)

mask = (df['order_purchase_timestamp'] >= pd.to_datetime(start)) & \
       (df['order_purchase_timestamp'] <= pd.to_datetime(end))

df = df[mask]

if df.empty:
    st.warning("Data kosong untuk filter ini")
    st.stop()

# ======================
# TITLE
# ======================
st.title("📊 E-Commerce Dashboard")

# ======================
# Q1 PAYMENT
# ======================
st.header("💳 Metode Pembayaran")

payment = df.groupby("payment_type")["payment_value"].sum().sort_values(ascending=False)

st.bar_chart(payment)
st.info(f"Dominan: {payment.idxmax()}")

# ======================
# Q2 SELLER
# ======================
st.header("🏪 Top Seller")

seller = df["seller_id"].value_counts().head(10)

st.bar_chart(seller)

# ======================
# INSIGHT
# ======================
st.markdown("### 📌 Insight")
st.write("""
- Payment didominasi metode tertentu
- Penjualan sangat terkonsentrasi pada seller tertentu (Pareto)
- Distribusi seller tidak merata
""")
