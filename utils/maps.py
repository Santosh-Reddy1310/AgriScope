# utils/maps.py

import json
import pandas as pd
import plotly.express as px
import streamlit as st

def plot_state_choropleth(data, mode='Production'):
    # Load geo data
    with open("data/india_states.geojson", "r") as f:
        india_geo = json.load(f)

    # Prepare data
    state_data = data.groupby("Region")[[mode]].mean().reset_index()
    state_data.columns = ["State", mode]

    fig = px.choropleth(
        state_data,
        geojson=india_geo,
        featureidkey="properties.NAME_1",
        locations="State",
        color=mode,
        color_continuous_scale="YlGnBu" if mode == "Rainfall" else "Greens",
        title=f"🗺️ State-wise Average {mode}",
    )
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r":0,"t":40,"l":0,"b":0})
    st.plotly_chart(fig, use_container_width=True)
