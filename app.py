import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# ========= SETUP =========
st.set_page_config(page_title="Sales BI Dashboard", layout="wide")
st.title("Sales Dashboard - BI Style")

# ========= DỮ LIỆU GIẢ =========
np.random.seed(42)
dates = pd.date_range(start="2024-01-01", end="2024-06-30", freq='D')
products = ["Laptop", "Mouse", "Keyboard", "Monitor", "Headphones", "Tablet"]
data = {
    "Date": np.random.choice(dates, 300),
    "Product": np.random.choice(products, 300),
    "CustomerID": np.random.randint(1000, 1100, 300),
    "Revenue": np.random.randint(50, 1500, 300)
}
df = pd.DataFrame(data)

# ========= SIDEBAR =========
st.sidebar.header("Bộ lọc")
selected_product = st.sidebar.multiselect("Chọn sản phẩm", options=products, default=products)
selected_date = st.sidebar.date_input("Chọn khoảng thời gian", [df["Date"].min(), df["Date"].max()])

# ========= FILTER =========
df_filtered = df[
    (df["Product"].isin(selected_product)) &
    (df["Date"] >= pd.to_datetime(selected_date[0])) &
    (df["Date"] <= pd.to_datetime(selected_date[1]))
]

# ========= KPI =========
total_revenue = df_filtered["Revenue"].sum()
total_orders = df_filtered.shape[0]
unique_customers = df_filtered["CustomerID"].nunique()

st.markdown("### KPIs Tổng quan")
col1, col2, col3 = st.columns(3)
col1.metric("Doanh thu", f"${total_revenue:,.0f}")
col2.metric("Số đơn hàng", total_orders)
col3.metric("Khách hàng", unique_customers)

st.markdown("---")

# ========= BIỂU ĐỒ DOANH THU THEO THỜI GIAN =========
revenue_by_date = df_filtered.groupby("Date")["Revenue"].sum().reset_index()
fig1 = px.line(revenue_by_date, x="Date", y="Revenue", title="Doanh thu theo thời gian", markers=True)
fig1.update_layout(hovermode="x unified")

# ========= BIỂU ĐỒ TOP SẢN PHẨM =========
top_product = df_filtered.groupby("Product")["Revenue"].sum().sort_values(ascending=False).reset_index()
fig2 = px.bar(top_product, x="Product", y="Revenue", title=" Doanh thu theo sản phẩm", color="Product")

# ========= HIỂN THỊ =========
col4, col5 = st.columns(2)
col4.plotly_chart(fig1, use_container_width=True)
col5.plotly_chart(fig2, use_container_width=True)

# ========= TABLE CHI TIẾT =========
st.markdown("### Bảng dữ liệu chi tiết")
st.dataframe(df_filtered.sort_values(by="Date", ascending=False), use_container_width=True)
