from pathlib import Path
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="E-Commerce Dashboard", layout="wide")

# ======================
# PATH FIX
# ======================
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR.parent / "data"


@st.cache_data
def load(file):
    return pd.read_csv(DATA_DIR / file)


# ======================
# LOAD DATA
# ======================
orders = load("orders_dataset.csv")[["order_id", "order_purchase_timestamp"]]
items = load("order_items_dataset.csv")[["order_id", "price", "seller_id"]]
payments = load("order_payments_dataset.csv")[["order_id", "payment_value", "payment_type"]]
reviews = load("order_reviews_dataset.csv")[["order_id", "review_score"]]
products = load("products_dataset.csv")[["product_id", "product_category_name"]]


# ======================
# PREPROCESS
# ======================
orders["order_purchase_timestamp"] = pd.to_datetime(
    orders["order_purchase_timestamp"],
    errors="coerce"
)

orders = orders.dropna(subset=["order_purchase_timestamp"])


# ======================
# FILTER (SEBELUM MERGE = WAJIB)
# ======================
st.sidebar.header("Filter")

min_date = orders["order_purchase_timestamp"].min()
max_date = orders["order_purchase_timestamp"].max()

date_range = st.sidebar.date_input(
    "Tanggal",
    value=[min_date, max_date]
)

if len(date_range) != 2:
    st.stop()

start, end = date_range

orders = orders[
    (orders["order_purchase_timestamp"] >= pd.to_datetime(start)) &
    (orders["order_purchase_timestamp"] <= pd.to_datetime(end))
]


# ======================
# AGGREGASI (INI KUNCI HEMAT MEMORY)
# ======================

# Orders + Items (ringkasan)
items_agg = items.groupby("order_id").agg({
    "price": "sum",
    "seller_id": "first"
}).reset_index()

# Payments (ringkasan)
pay_agg = payments.groupby("order_id").agg({
    "payment_value": "sum",
    "payment_type": "first"
}).reset_index()

# Reviews (ringkasan)
rev_agg = reviews.groupby("order_id").agg({
    "review_score": "mean"
}).reset_index()


# ======================
# MERGE RINGAN SAJA
# ======================
df = orders.merge(items_agg, on="order_id", how="left")
df = df.merge(pay_agg, on="order_id", how="left")
df = df.merge(rev_agg, on="order_id", how="left")


# ======================
# CLEAN
# ======================
df = df.drop_duplicates()


# ======================
# UI
# ======================
st.title("📊 E-Commerce Dashboard (Ultra Light Version)")


col1, col2, col3 = st.columns(3)

col1.metric("Orders", df["order_id"].nunique())
col2.metric("Revenue", df["payment_value"].sum())
col3.metric("Avg Review", df["review_score"].mean())


# ======================
# PAYMENT
# ======================
st.subheader("Payment Method")

payment = df["payment_type"].value_counts()

fig, ax = plt.subplots()
payment.plot(kind="bar", ax=ax)
st.pyplot(fig)


# ======================
# TOP SELLER
# ======================
st.subheader("Top Seller")

seller = df.groupby("seller_id")["price"].sum().nlargest(10)

fig, ax = plt.subplots()
seller.plot(kind="bar", ax=ax)
st.pyplot(fig)


# ======================
# REVIEW
# ======================
st.subheader("Review Score")

review = df["review_score"].value_counts().sort_index()

fig, ax = plt.subplots()
review.plot(kind="bar", ax=ax)
st.pyplot(fig)
