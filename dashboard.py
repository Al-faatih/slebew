import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ========================
# LOAD DATA
# ========================
orders = pd.read_csv('data/orders_dataset.csv')
order_items = pd.read_csv('data/order_items_dataset.csv')
products = pd.read_csv('data/products_dataset.csv')
payments = pd.read_csv('data/order_payments_dataset.csv')

# ========================
# PREPROCESSING
# ========================
orders['order_purchase_timestamp'] = pd.to_datetime(orders['order_purchase_timestamp'])

# Merge data
df = orders.merge(order_items, on='order_id')
df = df.merge(products, on='product_id')
df = df.merge(payments, on='order_id')

# ========================
# SIDEBAR FILTER
# ========================
st.sidebar.title("Filter Data")

start_date = st.sidebar.date_input("Start Date", orders['order_purchase_timestamp'].min())
end_date = st.sidebar.date_input("End Date", orders['order_purchase_timestamp'].max())

filtered_df = df[
    (df['order_purchase_timestamp'] >= pd.to_datetime(start_date)) &
    (df['order_purchase_timestamp'] <= pd.to_datetime(end_date))
]

# ========================
# TITLE
# ========================
st.title(" E-Commerce Dashboard")


# Metode Pembayaran
# ========================
st.header("Metode Pembayaran & Nilai Transaksi")

payment_summary = filtered_df.groupby('payment_type')['payment_value'].sum().sort_values(ascending=False)

st.subheader("Total Payment Value per Method")
st.bar_chart(payment_summary)

# Insight singkat
top_payment = payment_summary.idxmax()
st.info(f"Metode pembayaran paling dominan: **{top_payment}**")


st.header("Top Seller & Kontribusi")

seller_summary = filtered_df.groupby('seller_id')['order_id'].count().sort_values(ascending=False).head(10)

st.subheader("Top 10 Seller by Orders")
st.bar_chart(seller_summary)


st.subheader("Distribusi Kontribusi Seller")

seller_dist = filtered_df.groupby('seller_id')['order_id'].count()
seller_dist = seller_dist.sort_values(ascending=False)

plt.figure()
plt.plot(seller_dist.values[:50])
plt.title("Distribusi Seller (Top 50)")
st.pyplot(plt)

# ========================
# FOOTER INSIGHT
# ========================
st.markdown("---")
st.subheader(" Insight Singkat")

st.write("""
- Metode pembayaran tertentu mendominasi transaksi.
- Sebagian kecil seller menyumbang mayoritas penjualan (Pareto).
- Terdapat ketimpangan kontribusi antar seller.
""")