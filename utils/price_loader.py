import pandas as pd
import streamlit as st

@st.cache_data
def load_price_data():
    df = pd.read_csv("data/crop_prices.csv")

    # Rename properly
    df = df.rename(columns={
        "Modal_x0020_Price": "price",
        "Arrival_Date": "date",
        "Commodity": "commodity"
    })

    # Clean dates
    df["date"] = pd.to_datetime(df["date"], errors='coerce')
    df = df.dropna(subset=["date"])
    df["year"] = df["date"].dt.year

    # Normalize commodity names
    df["commodity_clean"] = df["commodity"].str.strip().str.lower()

    return df[["State", "District", "Market", "commodity", "commodity_clean", "price", "date", "year"]]
