import streamlit as st
import pandas as pd

from utils.data_loader import load_crop_data
from utils.price_loader import load_price_data
from utils.rainfall_loader import load_rainfall_data
from utils.gemini_ai import (
    generate_summary,
    get_live_crop_price,
    predict_future_trend_with_gemini,
)
from utils.pdf_exporter import export_to_pdf
from utils.geo_plot import plot_choropleth
from utils.charts import (
    plot_crop_trends,
    plot_region_probability,
    plot_rainfall_vs_production,
)

# ------------------- PAGE SETUP ---------------------
st.set_page_config(page_title="AgriScope", layout="wide")
st.title("🌾 AgriScope – India Crop Intelligence Dashboard")
st.markdown("Empowering agriculture students with smart, visual, and AI-driven insights.")
st.markdown("---")

# ------------------- LOAD DATA ---------------------
crop_data = load_crop_data()
price_data = load_price_data()
rain_data = load_rainfall_data()

# 🔧 State name fixes for choropleth match
state_name_map = {
    "Orissa": "Odisha",
    "Chattisgarh": "Chhattisgarh",
    "Uttaranchal": "Uttarakhand",
    "Delhi": "Delhi",
    "Jammu & Kashmir": "Jammu and Kashmir",
}

crop_data["Region"] = crop_data["Region"].replace(state_name_map)

# ------------------- SIDEBAR FILTERS ---------------------
st.sidebar.header("🔎 Filters")
region = st.sidebar.selectbox("Select Region (State)", sorted(crop_data["Region"].unique()))
crop1 = st.sidebar.selectbox("Crop 1", sorted(crop_data["Crop"].unique()))
crop2 = st.sidebar.selectbox("Crop 2", sorted(crop_data["Crop"].unique()))

# Filter data
region_data = crop_data[crop_data["Region"] == region]
crops_to_plot = region_data[region_data["Crop"].isin([crop1, crop2])]

# 🔄 Rainfall region matching
region_key = region.lower().replace(" ", "").replace("&", "and")
rain_data["MatchKey"] = rain_data["Region"].str.lower().str.replace(" ", "").str.replace("&", "and")
region_rain = rain_data[rain_data["MatchKey"].str.contains(region_key)]

# ------------------- VISUALIZATIONS ---------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader(f"📊 Crop Trends in {region}")
    plot_crop_trends(crops_to_plot)

with col2:
    st.subheader("🌱 Avg Production in Region")
    plot_region_probability(region_data)

st.markdown("---")

col3, col4 = st.columns(2)

with col3:
    st.subheader("🌧️ Rainfall vs Production")
    if region_rain.empty:
        st.warning("No rainfall data found for this region.")
    else:
        plot_rainfall_vs_production(region_rain, region_data)

with col4:
    st.subheader(f"💹 AI Market Trends for {crop1}")
    if st.button("🧠 Get Live Market Price"):
        with st.spinner("Gemini fetching mandi prices..."):
            st.session_state["market_price_summary"] = get_live_crop_price(crop1)

    if "market_price_summary" in st.session_state:
        st.success("✅ Fetched current price info!")
        st.markdown(st.session_state["market_price_summary"])

st.markdown("---")

# ------------------- AI SUMMARY + EXPORT ---------------------
st.subheader("🧠 AI Insight Summary + Export")
col5, col6 = st.columns([3, 2])

with col5:
    if st.button("✨ Generate Gemini AI Summary"):
        with st.spinner("Gemini analyzing agri data... 🌾🧠"):
            summary = generate_summary(region, crops_to_plot, region_rain)
            st.session_state["ai_summary"] = summary

    if "ai_summary" in st.session_state:
        st.success("✅ AI Summary Generated")
        st.markdown(st.session_state["ai_summary"])
    else:
        st.info("Click above to generate an AI-powered insight for this region & crops.")

with col6:
    if st.button("📄 Export PDF Report"):
        path = export_to_pdf(region, crops_to_plot)
        st.success(f"✅ Report saved to: {path}")
        with open(path, "rb") as f:
            st.download_button("⬇️ Download Report", f, file_name="AgriScope_Report.pdf")

# ------------------- CHOROPLETH MAP ---------------------
st.markdown("---")
st.subheader("🗺️ Region-wise Crop Production Map")

geojson_path = "data/india_states.geojson"
try:
    choropleth_fig = plot_choropleth(crop_data, geojson_path, crop1)
    st.plotly_chart(choropleth_fig, use_container_width=True)
except Exception as e:
    st.error(f"Failed to render choropleth map: {e}")

# ------------------- FUTURE TREND FORECAST ---------------------
st.markdown("---")
st.subheader("📈 AI-Powered Future Trend Forecast")

if st.button("🔮 Predict Future Trends with Gemini"):
    with st.spinner("Gemini analyzing future patterns..."):
        future_forecast = predict_future_trend_with_gemini(region, crop1, region_data)
        st.markdown(future_forecast)

# ------------------- FOOTER ---------------------
st.caption("Built with ❤️ for Indian Agriculture – Powered by Streamlit & Gemini 1.5 Flash")
