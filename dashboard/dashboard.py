import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

# ========================
# CONFIG
# ========================
st.set_page_config(page_title="E-Commerce Dashboard", layout="wide")

# ========================
# LOAD DATA (STREAMLIT SAFE)
# ========================
BASE_DIR = os.path.dirname(__file__)

orders = pd.read_csv(os.path.join(BASE_DIR, "data/orders_dataset.csv"))
order_items = pd.read_csv(os.path.join(BASE_DIR, "data/order_items_dataset.csv"))
products = pd.read_csv(os.path.join(BASE_DIR, "data/products_dataset.csv"))
payments = pd.read_csv(os.path.join(BASE_DIR, "data/order_payments_dataset.csv"))

# ========================
# PREPROCESS
# ========================
orders["order_purchase_timestamp"] = pd.to_datetime(
    orders["order_purchase_timestamp"], errors="coerce"
)

payments_agg = payments.groupby("order_id", as_index=False)["payment_value"].sum()

df = orders.merge(order_items, on="order_id", how="inner")
df = df.merge(products, on="product_id", how="inner")
df = df.merge(payments_agg, on="order_id", how="inner")

# ========================
# FILTER
# ========================
st.sidebar.title("Filter Waktu")

min_date = orders["order_purchase_timestamp"].min()
max_date = orders["order_purchase_timestamp"].max()

start_date = st.sidebar.date_input("Start", min_date)
end_date = st.sidebar.date_input("End", max_date)

filtered_df = df[
    (df["order_purchase_timestamp"] >= pd.to_datetime(start_date)) &
    (df["order_purchase_timestamp"] <= pd.to_datetime(end_date))
]

if filtered_df.empty:
    st.warning("Data kosong untuk filter ini")
    st.stop()

# ========================
# TITLE
# ========================
st.title("📊 E-Commerce Dashboard")

# ======================================================
# 💳 PERTANYAAN 1
# ======================================================
st.header("💳 Payment Method vs Transaction Value")

payment_summary = (
    filtered_df.groupby("payment_type")["payment_value"]
    .sum()
    .sort_values(ascending=False)
)

st.bar_chart(payment_summary)

st.success(f"Metode dominan: {payment_summary.idxmax()}")

# ======================================================
# 🏪 PERTANYAAN 2
# ======================================================
st.header("🏪 Top Seller Performance")

seller_summary = (
    filtered_df.groupby("seller_id")["order_id"]
    .count()
    .sort_values(ascending=False)
    .head(10)
)

st.bar_chart(seller_summary)

# ========================
# INSIGHT
# ========================
st.markdown("---")
st.subheader("📌 Insight")

st.write("""
- Metode pembayaran tertentu paling dominan dalam transaksi.
- Penjualan sangat terkonsentrasi pada beberapa seller (Pareto 80/20).
- Distribusi seller tidak merata → perlu strategi pemerataan performa.
""")
