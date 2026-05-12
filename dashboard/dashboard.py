import os
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="E-Commerce Dashboard", layout="wide")

# ======================
# PATH SETUP (PENTING)
# ======================
LOCAL_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.abspath(os.path.join(LOCAL_DIR, ".."))

# ======================
# LOAD DATA FUNCTION
# ======================
@st.cache_data
def load_data(filename):
    path = os.path.join(BASE_DIR, filename)

    if not os.path.exists(path):
        st.error(f"❌ File tidak ditemukan: {filename}")
        st.stop()

    if os.stat(path).st_size == 0:
        st.error(f"❌ File kosong: {filename}")
        st.stop()

    return pd.read_csv(path)

# ======================
# LOAD SEMUA DATA
# ======================
orders = load_data("orders_dataset.csv")
order_items = load_data("order_items_dataset.csv")
products = load_data("products_dataset.csv")
payments = load_data("order_payments_dataset.csv")
customers = load_data("customers_dataset.csv")

# ======================
# PREPROCESSING
# ======================
orders['order_purchase_timestamp'] = pd.to_datetime(
    orders['order_purchase_timestamp'],
    errors='coerce'
)

orders = orders.dropna(subset=['order_purchase_timestamp'])

# ======================
# SIDEBAR FILTER
# ======================
st.sidebar.header("📌 Filter Data")

min_date = orders['order_purchase_timestamp'].min()
max_date = orders['order_purchase_timestamp'].max()

date_range = st.sidebar.date_input(
    "Pilih Rentang Tanggal",
    value=[min_date, max_date]
)

# Handle jika user tidak pilih lengkap
if len(date_range) != 2:
    st.warning("⚠️ Pilih rentang tanggal dengan benar")
    st.stop()

start_date, end_date = date_range

filtered_orders = orders[
    (orders['order_purchase_timestamp'] >= pd.to_datetime(start_date)) &
    (orders['order_purchase_timestamp'] <= pd.to_datetime(end_date))
]

if filtered_orders.empty:
    st.warning("⚠️ Data kosong pada rentang tanggal ini")
    st.stop()

# ======================
# TITLE
# ======================
st.title("📊 E-Commerce Data Analysis Dashboard")

# ======================
# METRICS
# ======================
st.subheader("📌 Key Metrics")

col1, col2 = st.columns(2)

col1.metric("Total Orders", filtered_orders['order_id'].nunique())
col2.metric("Total Customers", filtered_orders['customer_id'].nunique())

# ======================
# METODE PEMBAYARAN
# ======================
st.subheader("💳 Metode Pembayaran Terpopuler")

payments_filtered = payments[
    payments['order_id'].isin(filtered_orders['order_id'])
]

if payments_filtered.empty:
    st.warning("⚠️ Tidak ada data pembayaran")
else:
    payment_counts = payments_filtered['payment_type'].value_counts()

    fig1, ax1 = plt.subplots()
    payment_counts.plot(kind='bar', ax=ax1)
    ax1.set_title("Distribusi Metode Pembayaran")
    ax1.set_xlabel("Metode")
    ax1.set_ylabel("Jumlah")
    plt.xticks(rotation=30)

    st.pyplot(fig1)

# ======================
# TOP SELLER
# ======================
st.subheader("🏪 Top Seller Berdasarkan Penjualan")

merged_data = order_items.merge(
    filtered_orders[['order_id']],
    on='order_id',
    how='inner'
)

if merged_data.empty:
    st.warning("⚠️ Tidak ada data seller")
else:
    top_sellers = merged_data.groupby('seller_id')['price'] \
        .sum() \
        .sort_values(ascending=False) \
        .head(10)

    fig2, ax2 = plt.subplots()
    top_sellers.plot(kind='bar', ax=ax2)
    ax2.set_title("Top 10 Seller")
    ax2.set_xlabel("Seller ID")
    ax2.set_ylabel("Total Penjualan")
    plt.xticks(rotation=45)

    st.pyplot(fig2)

# ======================
# DATA PREVIEW
# ======================
st.subheader("📄 Preview Data")
st.dataframe(filtered_orders.head())

# ======================
# INSIGHT
# ======================
st.subheader("💡 Insight")

st.write("""
- Metode pembayaran tertentu mendominasi transaksi  
- Seller top berkontribusi besar terhadap revenue  
- Distribusi penjualan tidak merata  
""")

# ======================
# RECOMMENDATION
# ======================
st.subheader("🚀 Recommendations")

st.write("""
1. Fokus pada metode pembayaran populer  
2. Pertahankan seller top performer  
3. Evaluasi seller dengan performa rendah  
4. Optimalkan strategi pemasaran berbasis data  
""")
