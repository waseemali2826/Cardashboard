import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Page configuration
st.set_page_config(page_title="Car Listings Dashboard", layout="wide")

# Sample cars data
np.random.seed(0)
brands = ["Toyota", "Honda", "BMW", "Mercedes", "Ford"]
cars = pd.DataFrame({
    "Brand": np.random.choice(brands, 200),
    "Price": np.random.randint(15000, 80000, 200),
    "Mileage": np.random.randint(5, 20, 200),
    "Year": np.random.randint(2010, 2024, 200)
})
# Sidebar filters
st.sidebar.header("Filter Cars")
selected_brand = st.sidebar.multiselect("Select Brand(s)", options=cars["Brand"].unique(), default=cars["Brand"].unique())
year_range = st.sidebar.slider("Select Year Range", int(cars["Year"].min()), int(cars["Year"].max()), (2012, 2023))

# Apply filters
filtered_cars = cars[
    (cars["Brand"].isin(selected_brand)) &
    (cars["Year"] >= year_range[0]) & (cars["Year"] <= year_range[1])
]
# Title
st.title("🚗 Car Listings Dashboard")
# KPIs
st.subheader("📌 Key Metrics")
col1, col2, col3 = st.columns(3)
col1.metric("Total Cars", len(filtered_cars))
col2.metric("Average Price", f"${filtered_cars['Price'].mean():,.0f}")
col3.metric("Avg. Mileage (km/l)", f"{filtered_cars['Mileage'].mean():.2f}")

# Price Distribution
st.subheader("💰 Price Distribution")
fig1, ax1 = plt.subplots()
ax1.hist(filtered_cars["Price"], bins=15, color="skyblue", edgecolor="black")
ax1.set_xlabel("Price ($)")
ax1.set_ylabel("Number of Cars")
st.pyplot(fig1)

# Mileage by Brand
st.subheader("⚙️ Average Mileage by Brand")
mileage_by_brand = filtered_cars.groupby("Brand")["Mileage"].mean().sort_values()
fig2, ax2 = plt.subplots()
mileage_by_brand.plot(kind="barh", ax=ax2, color="lightgreen")
ax2.set_xlabel("Mileage (km/l)")
st.pyplot(fig2)

# Show raw data
with st.expander("📄 Show Raw Data"):
    st.dataframe(filtered_cars)
