import json
import plotly.express as px

def plot_choropleth(crop_data, geojson_path, selected_crop):
    # Prepare the data
    crop_avg = (
        crop_data[crop_data["Crop"] == selected_crop]
        .groupby("Region")["Production (1000 tons)"]
        .mean()
        .reset_index()
    )
    crop_avg.columns = ["Region", "Avg Production"]

    # Load GeoJSON
    with open(geojson_path, "r", encoding="utf-8") as f:
        india_geo = json.load(f)

    # Get all state names from the geojson
    geo_states = [f["properties"]["NAME_1"] for f in india_geo["features"]]

    # Filter only matching regions
    crop_avg = crop_avg[crop_avg["Region"].isin(geo_states)]

    # Plot map
    fig = px.choropleth(
        crop_avg,
        geojson=india_geo,
        locations="Region",
        featureidkey="properties.NAME_1",  # <- FIXED LINE
        color="Avg Production",
        color_continuous_scale="YlGn",
        title=f"{selected_crop} Production by State",
        height=600,
    )

    fig.update_geos(fitbounds="locations", visible=True)
    fig.update_layout(margin={"r":0,"t":30,"l":0,"b":0})

    return fig
