import os
import streamlit as st
import google.generativeai as genai
import pandas as pd
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel("models/gemini-1.5-flash")

def generate_summary(region: str, data: pd.DataFrame, rain_data: pd.DataFrame = None) -> str:
    crops = data["Crop"].unique().tolist()
    summary_data = {}

    for crop in crops:
        crop_df = data[data["Crop"] == crop]
        avg_production = crop_df["Production (1000 tons)"].mean()
        peak_year = crop_df.loc[crop_df["Production (1000 tons)"].idxmax(), "Year"]
        summary_data[crop] = {
            "avg_production": round(avg_production, 2),
            "peak_year": int(peak_year)
        }

    # Basic prompt
    prompt = f"""You're an expert agriculture analyst. Analyze this Indian crop production data for the region: {region}.

Here are the crops and their stats:\n"""

    for crop, stats in summary_data.items():
        prompt += f"- {crop}: Avg production = {stats['avg_production']}k tons, Peak year = {stats['peak_year']}\n"

    # Add rainfall summary if provided
    if rain_data is not None and not rain_data.empty:
        rain_avg = rain_data["Rainfall"].mean()
        prompt += f"\nAverage annual rainfall in this region is around {rain_avg:.2f} mm.\n"
        prompt += """Based on this, analyze how rainfall might be affecting crop production patterns.
Highlight any trends, correlations, or surprising observations if visible.\n"""

    prompt += "\nProvide a short and insightful summary (in markdown)."

    response = model.generate_content(prompt)
    return response.text.strip()
def get_live_crop_price(crop: str):
    prompt = f"""
    You are an agri price analyst. Give a brief summary of the current market price range of '{crop}' in India.
    Include:
    - Price per quintal (INR)
    - Major mandi locations
    - Trends (rising/falling)
    Be concise and clear for agriculture students.
    """

    response = model.generate_content(prompt)
    return response.text.strip()


def predict_future_trend_with_gemini(region: str, crop: str, data: pd.DataFrame) -> str:
    # Prepare crop stats
    crop_df = data[data["Crop"] == crop]
    if crop_df.empty:
        return f"⚠️ No historical data available for {crop} in {region}."

    avg_production = crop_df["Production (1000 tons)"].mean()
    peak_year = crop_df.loc[crop_df["Production (1000 tons)"].idxmax(), "Year"]
    recent_year = crop_df["Year"].max()
    recent_production = crop_df[crop_df["Year"] == recent_year]["Production (1000 tons)"].values[0]

    prompt = f"""
    You're an expert agricultural futurist. Based on historical crop production data in {region}, forecast the future trend of {crop} over the next 5 years.

    Context:
    - Region: {region}
    - Crop: {crop}
    - Avg Production: {avg_production:.2f}k tons
    - Peak Year: {peak_year}
    - Most recent year: {recent_year}, Production: {recent_production:.2f}k tons

    Predict:
    - Is the crop likely to increase or decrease in production?
    - Any environmental or market factors that may influence this?
    - A production forecast table for the next 5 years.
    - Make it easy to understand for agriculture students.

    Format in markdown.
    """

    response = model.generate_content(prompt)
    return response.text.strip()
