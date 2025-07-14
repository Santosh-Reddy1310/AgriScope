import pandas as pd
import streamlit as st

@st.cache_data
def load_crop_data():
    df = pd.read_csv("data/crop_production.csv")
    df.columns = [col.strip().upper() for col in df.columns]

    id_cols = ["YEAR", "STATE NAME", "DIST NAME"]
    crop_cols = [col for col in df.columns if any(x in col for x in ["AREA", "PRODUCTION", "YIELD"])]

    df_long = pd.melt(df, id_vars=id_cols, value_vars=crop_cols,
                      var_name="Feature", value_name="Value")

    df_long["Feature"] = df_long["Feature"].str.replace("  ", " ").str.strip()
    df_long[["Crop", "Metric"]] = df_long["Feature"].str.extract(r'^(.*) (AREA|PRODUCTION|YIELD)')

    df_pivot = df_long.pivot_table(index=["YEAR", "STATE NAME", "DIST NAME", "Crop"],
                                   columns="Metric", values="Value", aggfunc="first").reset_index()

    df_pivot = df_pivot.rename(columns={
        "YEAR": "Year",
        "STATE NAME": "Region",
        "DIST NAME": "District",
        "AREA": "Area (1000 ha)",
        "PRODUCTION": "Production (1000 tons)",
        "YIELD": "Yield (Kg/ha)"
    })

    df_pivot = df_pivot[df_pivot["Crop"].notna()]
    df_pivot["Crop"] = df_pivot["Crop"].str.title()
    df_pivot = df_pivot[df_pivot["Production (1000 tons)"].notna()]
    return df_pivot
