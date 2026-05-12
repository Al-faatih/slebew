from pathlib import Path
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="E-Commerce Dashboard", layout="wide")

# ======================
# PATH SETUP
# ======================
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"


# ======================
# LOAD DATA (CACHE)
# ======================
@st.cache_data
def load_data(file):
    return pd.read_csv(DATA_DIR / file)


# ======================
# LOAD DATASET (ONLY NEEDED COLUMNS)
# ======================

orders = load_data("orders_dataset.csv")[[
    "order_id",
    "customer_id",
    "order_purchase_timestamp"
]]

order_items = load_data("order_items_dataset.csv")[[
    "order_id",
    "price",
    "seller_id",
    "product_id"
]]

payments = load_data("order_payments_dataset.csv")[[
    "order_id",
    "payment_type",
    "payment_value"
]]

products = load_data("products_dataset.csv")[[
    "product_id",
    "product_category_name"
]]

category = load_data("product_category_name_translation.csv")

reviews = load_data("order_reviews_dataset.csv")[[
    "order_id",
    "review_score"
]]

customers = load_data("customers_dataset.csv")[[
    "customer_id"
]]


# ======================
# PREPROCESS
# ======================
orders["order_purchase_timestamp"] = pd.to_datetime(
    orders["order_purchase_timestamp"],
    errors="coerce"
)

orders = orders.dropna(subset=["order_purchase_timestamp"])


# ======================
# SIDEBAR FILTER (FILTER DULU = HEMAT RAM)
# ======================
st.sidebar.header("📌 Filter Data")

min_date = orders["order_purchase_timestamp"].min()
max_date = orders["order_purchase_timestamp"].max()

date_range = st.sidebar.date_input(
    "Pilih Rentang Tanggal",
    value=[min_date, max_date]
)

if len(date_range) != 2:
    st.warning("⚠️ Pilih rentang tanggal")
    st.stop()

start_date, end_date = date_range

orders = orders[
    (orders["order_purchase_timestamp"] >= pd.to_datetime(start_date)) &
    (orders["order_purchase_timestamp"] <= pd.to_datetime(end_date))
]


# ======================
# MERGE (SETELAH FILTER)
# ======================
df = orders.merge(order_items, on="order_id", how="left")
df = df.merge(payments, on="order_id", how="left")
df = df.merge(products, on="product_id", how="left")
df = df.merge(category, on="product_category_name", how="left")
df = df.merge(reviews, on="order_id", how="left")


# ======================
# CLEAN DATA
# ======================
df = df.drop_duplicates()


# ======================
# TITLE
# ======================
st.title("📊 E-Commerce Dashboard (Optimized & Safe)")


# ======================
# METRICS
# ======================
col1, col2, col3 = st.columns(3)

col1.metric("Total Orders", df["order_id"].nunique())
col2.metric("Total Customers", df["customer_id"].nunique())
col3.metric("Total Revenue", f"${df['payment_value'].sum():,.2f}")


# ======================
# PAYMENT ANALYSIS
# ======================
st.subheader("💳 Metode Pembayaran")

payment_counts = df["payment_type"].value_counts()

fig1, ax1 = plt.subplots()
payment_counts.plot(kind="bar", ax=ax1)
ax1.set_title("Payment Method")
plt.xticks(rotation=30)
st.pyplot(fig1)


# ======================
# TOP SELLER
# ======================
st.subheader("🏪 Top Seller")

top_seller = df.groupby("seller_id")["price"].sum().nlargest(10)

fig2, ax2 = plt.subplots()
top_seller.plot(kind="bar", ax=ax2)
ax2.set_title("Top Seller")
plt.xticks(rotation=45)
st.pyplot(fig2)


# ======================
# TOP CATEGORY
# ======================
st.subheader("🏆 Top Category")

top_category = df.groupby("product_category_name")["price"].sum().nlargest(10)

fig3, ax3 = plt.subplots()
top_category.plot(kind="bar", ax=ax3)
ax3.set_title("Top Category")
plt.xticks(rotation=45)
st.pyplot(fig3)


# ======================
# REVIEW SCORE
# ======================
st.subheader("⭐ Review Score")

review = df["review_score"].value_counts().sort_index()

fig4, ax4 = plt.subplots()
review.plot(kind="bar", ax=ax4)
ax4.set_title("Review Score Distribution")
plt.xticks(rotation=0)
st.pyplot(fig4)


# ======================
# MONTHLY TREND
# ======================
st.subheader("📈 Monthly Trend")

df["month"] = df["order_purchase_timestamp"].dt.to_period("M").astype(str)

monthly = df.groupby("month")["order_id"].nunique()

fig5, ax5 = plt.subplots()
monthly.plot(ax=ax5)
ax5.set_title("Monthly Orders")
plt.xticks(rotation=45)
st.pyplot(fig5)


# ======================
# DATA PREVIEW
# ======================
st.subheader("📄 Preview Data")
st.dataframe(df.head())


# ======================
# INSIGHT
# ======================
st.subheader("💡 Insight")

st.write("""
- Payment tertentu paling dominan  
- Seller tertentu mendominasi revenue  
- Kategori produk tertentu paling laris  
- Review cenderung tinggi  
""")


# ======================
# RECOMMENDATION
# ======================
st.subheader("🚀 Recommendation")

st.write("""
1. Fokus pada payment populer  
2. Optimalkan seller top  
3. Evaluasi produk dengan rating rendah  
4. Perkuat kategori terlaris  
""")
