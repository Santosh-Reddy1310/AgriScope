import streamlit as st
import plotly.express as px
import pandas as pd
def plot_crop_trends(data):
    fig = px.line(data, x='Year', y='Production (1000 tons)', color='Crop',
                  title='Year-wise Crop Production (in 1000 tons)')
    st.plotly_chart(fig, use_container_width=True)

def plot_region_probability(data):
    crop_avgs = data.groupby('Crop')['Production (1000 tons)'].mean().reset_index()
    fig = px.bar(crop_avgs, x='Crop', y='Production (1000 tons)', color='Crop',
                 title='Average Crop Production (1000 tons)')
    st.plotly_chart(fig, use_container_width=True)

def plot_rainfall_vs_production(rain_data, prod_data):
    if rain_data.empty or prod_data.empty:
        st.warning("Insufficient data for Rainfall or Production.")
        return

    # 1. Group production by year
    prod_avg = prod_data.groupby("Year")["Production (1000 tons)"].mean().reset_index()

    # 2. Group rainfall by year
    rain_avg = rain_data.groupby("Year")["Rainfall"].mean().reset_index()

    # 3. Merge them
    merged = pd.merge(prod_avg, rain_avg, on="Year", how="inner")

    # 4. Melt for plotting multiple y-values
    melted = merged.melt(id_vars="Year", value_vars=["Production (1000 tons)", "Rainfall"],
                         var_name="Metric", value_name="Amount")

    fig = px.line(melted, x="Year", y="Amount", color="Metric",
                  title="🌧️ Rainfall vs Crop Production Over Time")

    st.plotly_chart(fig, use_container_width=True)


def plot_price_trends(price_data, crop):
    crop = crop.strip().lower()
    
    filtered = price_data[price_data["commodity_clean"] == crop]

    if filtered.empty:
        st.warning(f"No price data found for '{crop.title()}' commodity.")
        return

    avg_by_year = filtered.groupby("year")["price"].mean().reset_index()

    fig = px.line(
        avg_by_year, x="year", y="price",
        title=f"💰 Average Price Trend for {crop.title()}",
        labels={"price": "Price (INR)", "year": "Year"}
    )

    st.plotly_chart(fig, use_container_width=True)
