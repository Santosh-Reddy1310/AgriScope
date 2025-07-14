import pandas as pd
import streamlit as st

def load_rainfall_data():
    df = pd.read_csv("data/Sub_Division_IMD_2017.csv")

    df.rename(columns={
        "SUBDIVISION": "Region",
        "YEAR": "Year",
        "ANNUAL": "Rainfall"
    }, inplace=True)

    df = df[["Region", "Year", "Rainfall"]]
    df["Year"] = df["Year"].astype(int)
    df["Rainfall"] = pd.to_numeric(df["Rainfall"], errors="coerce")
    df.dropna(inplace=True)

    # Normalize names for better matching
    df["Region"] = df["Region"].str.strip().str.title()

    # Add caching for performance
    return st.cache_data(lambda: df)()


    return df
