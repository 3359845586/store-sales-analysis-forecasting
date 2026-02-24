import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Superstore Dashboard", layout="wide")

st.title("📊 Superstore Sales Dashboard")

# ***************LOAD DATA
@st.cache_data
def load_data():
    df = pd.read_csv("store_dataset.csv", encoding="latin1")
    df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")
    return df

dataset = load_data()

# ************SIDEBAR FILTER
st.sidebar.header("🔎 Filter Data")

selected_regions = st.sidebar.multiselect(
    "Select Region",
    options=dataset["Region"].unique(),
    default=dataset["Region"].unique()
)

# Safe filtering
if len(selected_regions) > 0:
    filtered_data = dataset[dataset["Region"].isin(selected_regions)]
else:
    filtered_data = dataset.copy()

# *******************KPIs
total_sales = filtered_data["Sales"].sum()
total_profit = filtered_data["Profit"].sum()
profit_margin = (total_profit / total_sales) * 100 if total_sales != 0 else 0

col1, col2, col3 = st.columns(3)

col1.metric("Total Sales", f"${total_sales:,.0f}")
col2.metric("Total Profit", f"${total_profit:,.0f}")
col3.metric("Profit Margin", f"{profit_margin:.2f}%")

st.divider()

# *************** CHART SECTION
col1, col2 = st.columns(2)

# ---- Sales by Region ----
with col1:
    st.subheader("🌍 Sales by Region")
    region_sales = (
        filtered_data.groupby("Region")["Sales"]
        .sum()
        .sort_values()
    )

    fig1, ax1 = plt.subplots(figsize=(6, 4))
    region_sales.plot(kind="barh", ax=ax1)
    ax1.set_xlabel("Total Sales")
    ax1.set_ylabel("")
    plt.tight_layout()
    st.pyplot(fig1, use_container_width=True)

# ***********Monthly Sales Trend
with col2:
    st.subheader("📈 Monthly Sales Trend")
    monthly_sales = (
        filtered_data.resample("ME", on="Order Date")["Sales"]
        .sum()
    )

    fig2, ax2 = plt.subplots(figsize=(6, 4))
    monthly_sales.plot(ax=ax2)
    ax2.set_ylabel("Sales")
    plt.tight_layout()
    st.pyplot(fig2, use_container_width=True)

st.divider()

# ************TOP 10 PRODUCTS
st.subheader("🏆 Top 10 Products by Sales")

top_products = (
    filtered_data.groupby("Product Name")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

fig3, ax3 = plt.subplots(figsize=(10, 4))
top_products.plot(kind="bar", ax=ax3)
ax3.set_ylabel("Sales")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
st.pyplot(fig3, use_container_width=True)

#*********** Sales by Category
st.divider()

st.subheader("Sales by Category")

category_sales = (
    filtered_data.groupby("Category")["Sales"]
    .sum()
    .sort_values()
)

fig4, ax4 = plt.subplots(figsize=(6,4))
category_sales.plot(kind="barh", ax=ax4)
ax4.set_xlabel("Sales")
plt.tight_layout()
st.pyplot(fig4, use_container_width=True)

#*********8segment performance
st.subheader("👥 Sales by Customer Segment")

segment_sales = (
    filtered_data.groupby("Segment")["Sales"]
    .sum()
    .sort_values()
)

fig5, ax5 = plt.subplots(figsize=(6,4))
segment_sales.plot(kind="bar", ax=ax5)
plt.tight_layout()
st.pyplot(fig5, use_container_width=True)

#***********8Discount vs sales
st.subheader(" Discount vs Profit")

fig6, ax6 = plt.subplots(figsize=(6,4))
ax6.scatter(filtered_data["Discount"], filtered_data["Profit"])
ax6.set_xlabel("Discount")
ax6.set_ylabel("Profit")
plt.tight_layout()
st.pyplot(fig6, use_container_width=True)

# new change