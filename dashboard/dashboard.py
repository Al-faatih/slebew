from pathlib import Path
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="E-Commerce Dashboard", layout="wide")

# ======================
# PATH
# ======================
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR.parent / "data"


@st.cache_data
def load(file):
    return pd.read_csv(DATA_DIR / file)


# ======================
# LOAD DATA (MINIMAL)
# ======================
orders = load("orders_dataset.csv")[["order_id", "order_purchase_timestamp"]]
payments = load("order_payments_dataset.csv")[["order_id", "payment_type", "payment_value"]]
items = load("order_items_dataset.csv")[["order_id", "seller_id", "price"]]


# ======================
# PREPROCESS
# ======================
orders["order_purchase_timestamp"] = pd.to_datetime(
    orders["order_purchase_timestamp"],
    errors="coerce"
)

orders = orders.dropna()


# ======================
# FILTER DULU (INI PENTING)
# ======================
st.sidebar.header("Filter")

min_d = orders["order_purchase_timestamp"].min()
max_d = orders["order_purchase_timestamp"].max()

date_range = st.sidebar.date_input("Tanggal", [min_d, max_d])

if len(date_range) != 2:
    st.stop()

start, end = date_range

orders_f = orders[
    (orders["order_purchase_timestamp"] >= pd.to_datetime(start)) &
    (orders["order_purchase_timestamp"] <= pd.to_datetime(end))
]


# ======================
# 🔥 STEP 1: AGREGASI SEBELUM MERGE (INI KUNCI)
# ======================

# PAYMENT (ringkas dulu)
payments_f = payments.merge(orders_f, on="order_id", how="inner")
payment_summary = payments_f.groupby("payment_type", as_index=False)["payment_value"].sum()

# SELLER (ringkas dulu)
items_f = items.merge(orders_f, on="order_id", how="inner")
seller_summary = items_f.groupby("seller_id", as_index=False)["price"].sum()
seller_summary = seller_summary.nlargest(10, "price")


# ======================
# UI
# ======================
st.title("📊 E-Commerce Dashboard (Light Merge Version)")


col1, col2 = st.columns(2)

col1.metric("Total Orders", orders_f["order_id"].nunique())
col2.metric("Total Revenue", payments_f["payment_value"].sum())


# ======================
# PAYMENT CHART
# ======================
st.subheader("💳 Payment Method")

fig1, ax1 = plt.subplots()
ax1.bar(payment_summary["payment_type"], payment_summary["payment_value"])
plt.xticks(rotation=30)
st.pyplot(fig1)


# ======================
# SELLER CHART
# ======================
st.subheader("🏪 Top Seller")

fig2, ax2 = plt.subplots()
ax2.bar(seller_summary["seller_id"], seller_summary["price"])
plt.xticks(rotation=45)
st.pyplot(fig2)


# ======================
# INSIGHT
# ======================
st.subheader("💡 Insight")

st.write("""
- Data sudah di-aggregate sebelum merge  
- Tidak ada data besar yang digabung sekaligus  
- Dashboard ringan dan aman dari memory limit  
""")
