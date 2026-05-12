from pathlib import Path
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="E-Commerce Dashboard", layout="wide")

# ======================
# PATH SETUP (SESUAI STRUKTUR KAMU)
# ======================
BASE_DIR = Path(__file__).resolve().parent
ROOT_DIR = BASE_DIR.parent  # karena dashboard ada di folder dashboard/

# ======================
# LOAD DATA FUNCTION
# ======================
@st.cache_data
def load_data(filename):
    path = ROOT_DIR / filename

    if not path.exists():
        st.error(f"❌ File tidak ditemukan: {filename}")
        st.stop()

    if path.stat().st_size == 0:
        st.error(f"❌ File kosong: {filename}")
        st.stop()

    return pd.read_csv(path)


# ======================
# LOAD DATASET
# ======================
customers = load_data("customers_dataset.csv")
orders = load_data("orders_dataset.csv")
order_items = load_data("order_items_dataset.csv")
payments = load_data("order_payments_dataset.csv")
reviews = load_data("order_reviews_dataset.csv")
products = load_data("products_dataset.csv")
category = load_data("product_category_name_translation.csv")


# ======================
# PREPROCESSING
# ======================
orders['order_purchase_timestamp'] = pd.to_datetime(
    orders['order_purchase_timestamp'],
    errors='coerce'
)

orders = orders.dropna(subset=['order_purchase_timestamp'])


# ======================
# MERGE DATA
# ======================
df = orders.merge(customers, on="customer_id", how="left")
df = df.merge(order_items, on="order_id", how="left")
df = df.merge(payments, on="order_id", how="left")
df = df.merge(products, on="product_id", how="left")
df = df.merge(category, on="product_category_name", how="left")
df = df.merge(reviews, on="order_id", how="left")


# ======================
# SIDEBAR FILTER
# ======================
st.sidebar.header("📌 Filter Data")

min_date = df['order_purchase_timestamp'].min()
max_date = df['order_purchase_timestamp'].max()

date_range = st.sidebar.date_input(
    "Pilih Rentang Tanggal",
    value=[min_date, max_date]
)

if len(date_range) != 2:
    st.warning("⚠️ Pilih rentang tanggal dengan benar")
    st.stop()

start_date, end_date = date_range

df_filtered = df[
    (df['order_purchase_timestamp'] >= pd.to_datetime(start_date)) &
    (df['order_purchase_timestamp'] <= pd.to_datetime(end_date))
]

if df_filtered.empty:
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

col1, col2, col3 = st.columns(3)

col1.metric("Total Orders", df_filtered['order_id'].nunique())
col2.metric("Total Customers", df_filtered['customer_id'].nunique())
col3.metric("Total Revenue", f"${df_filtered['payment_value'].sum():,.2f}")


# ======================
# PAYMENT ANALYSIS
# ======================
st.subheader("💳 Metode Pembayaran Terpopuler")

payment_counts = df_filtered['payment_type'].value_counts()

fig1, ax1 = plt.subplots()
payment_counts.plot(kind='bar', ax=ax1)
ax1.set_title("Distribusi Metode Pembayaran")
plt.xticks(rotation=30)
st.pyplot(fig1)


# ======================
# TOP SELLER
# ======================
st.subheader("🏪 Top Seller")

top_sellers = df_filtered.groupby('seller_id')['price'].sum().sort_values(ascending=False).head(10)

fig2, ax2 = plt.subplots()
top_sellers.plot(kind='bar', ax=ax2)
ax2.set_title("Top 10 Seller")
plt.xticks(rotation=45)
st.pyplot(fig2)


# ======================
# TOP CATEGORY
# ======================
st.subheader("🏆 Top Kategori Produk")

top_category = df_filtered.groupby('product_category_name_english')['price'].sum().sort_values(ascending=False).head(10)

fig3, ax3 = plt.subplots()
top_category.plot(kind='bar', ax=ax3)
ax3.set_title("Top Kategori Produk")
plt.xticks(rotation=45)
st.pyplot(fig3)


# ======================
# REVIEW SCORE
# ======================
st.subheader("⭐ Distribusi Review Score")

review_counts = df_filtered['review_score'].value_counts().sort_index()

fig4, ax4 = plt.subplots()
review_counts.plot(kind='bar', ax=ax4)
ax4.set_title("Distribusi Rating")
plt.xticks(rotation=0)
st.pyplot(fig4)


# ======================
# MONTHLY TREND
# ======================
st.subheader("📈 Tren Order Bulanan")

df_filtered['month'] = df_filtered['order_purchase_timestamp'].dt.to_period('M').astype(str)

monthly_orders = df_filtered.groupby('month')['order_id'].nunique()

fig5, ax5 = plt.subplots()
monthly_orders.plot(ax=ax5)
ax5.set_title("Trend Order")
plt.xticks(rotation=45)
st.pyplot(fig5)


# ======================
# DATA PREVIEW
# ======================
st.subheader("📄 Preview Data")
st.dataframe(df_filtered.head())


# ======================
# INSIGHT
# ======================
st.subheader("💡 Insight")

st.write("""
- Metode pembayaran tertentu mendominasi transaksi  
- Seller top berkontribusi besar terhadap revenue  
- Kategori produk tertentu lebih laris  
- Mayoritas review berada di rating tinggi  
""")


# ======================
# RECOMMENDATION
# ======================
st.subheader("🚀 Recommendations")

st.write("""
1. Fokus pada metode pembayaran populer  
2. Pertahankan seller top performer  
3. Tingkatkan kualitas produk dengan rating rendah  
4. Optimalkan strategi penjualan kategori unggulan  
""")
