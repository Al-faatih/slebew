import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

# ========================
# PAGE CONFIG
# ========================
st.set_page_config(page_title="E-Commerce Dashboard", layout="wide")

# ========================
# LOAD DATA (CLOUD SAFE)
# ========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def load(file):
    return pd.read_csv(os.path.join(BASE_DIR, f"data/{file}"))

orders = load("orders_dataset.csv")
order_items = load("order_items_dataset.csv")
products = load("products_dataset.csv")
payments = load("order_payments_dataset.csv")

# ========================
# PREPROCESSING
# ========================
orders['order_purchase_timestamp'] = pd.to_datetime(
    orders['order_purchase_timestamp'], errors='coerce'
)

# DROP NULL DATE
orders = orders.dropna(subset=['order_purchase_timestamp'])

# ========================
# PAYMENT AGGREGATION (FIX DUPLICATE ISSUE)
# ========================
payments_agg = payments.groupby('order_id', as_index=False)['payment_value'].sum()

# ========================
# MERGE DATASET (BUSINESS READY)
# ========================
df = orders.merge(order_items, on='order_id', how='inner')
df = df.merge(products, on='product_id', how='inner')
df = df.merge(payments_agg, on='order_id', how='inner')

# ========================
# SIDEBAR FILTER
# ========================
st.sidebar.title("📅 Filter Data")

min_date = df['order_purchase_timestamp'].min().date()
max_date = df['order_purchase_timestamp'].max().date()

start_date = st.sidebar.date_input("Start Date", min_date)
end_date = st.sidebar.date_input("End Date", max_date)

filtered_df = df[
    (df['order_purchase_timestamp'].dt.date >= start_date) &
    (df['order_purchase_timestamp'].dt.date <= end_date)
]

# STOP IF EMPTY
if filtered_df.empty:
    st.warning("⚠️ Data tidak tersedia untuk filter ini")
    st.stop()

# ========================
# TITLE
# ========================
st.title("📊 E-Commerce Dashboard")

# ========================
# KPI DASHBOARD
# ========================
st.subheader("📌 Key Metrics")

col1, col2, col3 = st.columns(3)

col1.metric("💰 Total Revenue", f"{filtered_df['payment_value'].sum():,.0f}")
col2.metric("📦 Total Orders", filtered_df['order_id'].nunique())
col3.metric("🏪 Total Sellers", filtered_df['seller_id'].nunique())

# ========================
# PERTANYAAN 1
# PAYMENT ANALYSIS
# ========================
st.header("💳 Metode Pembayaran & Nilai Transaksi")

payment_summary = filtered_df.groupby('payment_type')['payment_value'].sum().sort_values(ascending=False)

st.bar_chart(payment_summary)

if not payment_summary.empty:
    st.info(f"💡 Metode pembayaran paling dominan: **{payment_summary.idxmax()}**")

# ========================
# PERTANYAAN 2
# SELLER ANALYSIS
# ========================
st.header("🏪 Top Seller Performance")

seller_summary = filtered_df.groupby('seller_id')['order_id'].count().sort_values(ascending=False).head(10)

st.bar_chart(seller_summary)

# ========================
# DISTRIBUSI SELLER
# ========================
st.subheader("📊 Distribusi Seller (Top 50)")

seller_dist = filtered_df['seller_id'].value_counts().head(50)

fig, ax = plt.subplots()
ax.plot(seller_dist.values)
ax.set_title("Top Seller Distribution")
ax.set_ylabel("Jumlah Order")
st.pyplot(fig)

# ========================
# INSIGHT
# ========================
st.markdown("---")
st.subheader("📌 Insight Bisnis")

st.write("""
- Metode pembayaran tertentu mendominasi transaksi dan menjadi pendorong utama revenue.
- Distribusi penjualan tidak merata (Pareto Principle): hanya sedikit seller yang menghasilkan mayoritas order.
- Terdapat peluang besar untuk meningkatkan performa seller menengah dan kecil.
- Optimasi metode pembayaran dan seller onboarding dapat meningkatkan total revenue.
""")
