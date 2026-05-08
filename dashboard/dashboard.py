import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

# ========================
# PAGE CONFIG
# ========================
st.set_page_config(page_title="E-Commerce Dashboard", layout="wide")

# ========================
# LOAD DATA (FIX PATH CLOUD SAFE)
# ========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

orders = pd.read_csv(os.path.join(BASE_DIR, 'data/orders_dataset.csv'))
order_items = pd.read_csv(os.path.join(BASE_DIR, 'data/order_items_dataset.csv'))
products = pd.read_csv(os.path.join(BASE_DIR, 'data/products_dataset.csv'))
payments = pd.read_csv(os.path.join(BASE_DIR, 'data/order_payments_dataset.csv'))

# ========================
# PREPROCESSING
# ========================
orders['order_purchase_timestamp'] = pd.to_datetime(orders['order_purchase_timestamp'])

# ========================
# MERGE DATA (SAFE JOIN)
# ========================
df = orders.merge(order_items, on='order_id', how='inner')
df = df.merge(products, on='product_id', how='inner')
df = df.merge(payments, on='order_id', how='inner')

# ========================
# FILTER DATE
# ========================
st.sidebar.title("Filter Data")

start_date = st.sidebar.date_input("Start Date", orders['order_purchase_timestamp'].min())
end_date = st.sidebar.date_input("End Date", orders['order_purchase_timestamp'].max())

filtered_df = df[
    (df['order_purchase_timestamp'] >= pd.to_datetime(start_date)) &
    (df['order_purchase_timestamp'] <= pd.to_datetime(end_date))
]

# STOP IF EMPTY
if filtered_df.empty:
    st.warning("Data tidak tersedia untuk filter ini")
    st.stop()

# ========================
# TITLE
# ========================
st.title("📊 E-Commerce Dashboard")

# ======================================================
# 📌 PERTANYAAN 1 - PAYMENT
# ======================================================
st.header("💳 Metode Pembayaran & Nilai Transaksi")

payment_summary = filtered_df.groupby('payment_type')['payment_value'].sum().sort_values(ascending=False)

st.bar_chart(payment_summary)

if not payment_summary.empty:
    st.info(f"Metode pembayaran dominan: **{payment_summary.idxmax()}**")

# ======================================================
# 📌 PERTANYAAN 2 - SELLER
# ======================================================
st.header("🏪 Top Seller")

seller_summary = filtered_df.groupby('seller_id')['order_id'].count().sort_values(ascending=False).head(10)

st.bar_chart(seller_summary)

# ========================
# DISTRIBUSI SELLER
# ========================
st.subheader("Distribusi Seller")

seller_dist = filtered_df['seller_id'].value_counts().head(50)

fig, ax = plt.subplots()
ax.plot(seller_dist.values)
ax.set_title("Top 50 Seller Distribution")
st.pyplot(fig)

# ========================
# INSIGHT
# ========================
st.markdown("---")
st.subheader("📌 Insight")

st.write("""
- Metode pembayaran tertentu mendominasi transaksi.
- Penjualan terkonsentrasi pada beberapa seller utama (Pareto).
- Terdapat ketimpangan kontribusi antar seller.
""")
