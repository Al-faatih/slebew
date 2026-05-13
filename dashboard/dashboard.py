from pathlib import Path
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# ======================
# CONFIG
# ======================
st.set_page_config(page_title="E-Commerce Dashboard", layout="wide")

# ======================
# PATH SETUP (AMAN REVIEWER)
# ======================
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR.parent / "data"


# ======================
# LOAD DATA FUNCTION
# ======================
@st.cache_data
def load_data(file):
    path = DATA_DIR / file

    if not path.exists():
        st.error(f"❌ File tidak ditemukan: {file}")
        st.stop()

    return pd.read_csv(path)


# ======================
# LOAD 3 DATASET SAJA
# ======================
orders = load_data("orders_dataset.csv")[[
    "order_id",
    "order_purchase_timestamp"
]]

payments = load_data("order_payments_dataset.csv")[[
    "order_id",
    "payment_type",
    "payment_value"
]]

order_items = load_data("order_items_dataset.csv")[[
    "order_id",
    "seller_id",
    "price"
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
# FILTER DATA (2017–2018)
# ======================
st.sidebar.header("📌 Filter Data")

min_date = orders["order_purchase_timestamp"].min()
max_date = orders["order_purchase_timestamp"].max()

date_range = st.sidebar.date_input(
    "Pilih Rentang Tanggal",
    value=[min_date, max_date]
)

if len(date_range) != 2:
    st.warning("Pilih rentang tanggal dengan benar")
    st.stop()

start_date, end_date = date_range

orders_filtered = orders[
    (orders["order_purchase_timestamp"] >= pd.to_datetime(start_date)) &
    (orders["order_purchase_timestamp"] <= pd.to_datetime(end_date))
]


# ======================
# PAYMENT ANALYSIS
# ======================
payment_df = orders_filtered.merge(payments, on="order_id", how="left")

payment_summary = payment_df.groupby("payment_type")["payment_value"].sum()


# ======================
# SELLER ANALYSIS
# ======================
seller_df = orders_filtered.merge(order_items, on="order_id", how="left")

seller_summary = seller_df.groupby("seller_id")["price"].sum().nlargest(10)


# ======================
# TITLE
# ======================
st.title("📊 E-Commerce Dashboard (3 Dataset - Optimized)")


# ======================
# METRICS
# ======================
col1, col2 = st.columns(2)

col1.metric("Total Orders", orders_filtered["order_id"].nunique())
col2.metric("Total Revenue", f"${payment_df['payment_value'].sum():,.2f}")


# ======================
# PAYMENT CHART
# ======================
st.subheader("💳 Metode Pembayaran Terpopuler")

fig1, ax1 = plt.subplots()
payment_summary.plot(kind="bar", ax=ax1)
ax1.set_title("Total Payment Value per Method")
plt.xticks(rotation=30)
st.pyplot(fig1)


# ======================
# SELLER CHART
# ======================
st.subheader("🏪 Top Seller")

fig2, ax2 = plt.subplots()
seller_summary.plot(kind="bar", ax=ax2)
ax2.set_title("Top 10 Seller by Revenue")
plt.xticks(rotation=45)
st.pyplot(fig2)


# ======================
# INSIGHT
# ======================
st.subheader("💡 Insight")

st.write("""
- Metode pembayaran tertentu menghasilkan nilai transaksi terbesar  
- Sebagian kecil seller mendominasi penjualan  
- Distribusi pendapatan tidak merata antar seller  
""")


# ======================
# DATA PREVIEW
# ======================
st.subheader("📄 Preview Data")

st.write("Payment Data")
st.dataframe(payment_df.head())

st.write("Seller Data")
st.dataframe(seller_df.head())
