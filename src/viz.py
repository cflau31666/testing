"""Visualization module."""
import plotly.express as px
import pandas as pd
import folium
from folium.plugins import HeatMap


# -------------------------------------
# 1. Line chart — hourly congestion
# -------------------------------------
def plot_hourly_line(df: pd.DataFrame, y: str = "congestion_index"):
    """Plot congestion or speed by hour."""
    fig = px.line(
        df,
        x="hour",
        y=y,
        markers=True,
        title="Traffic Congestion by Hour",
        labels={"hour": "Hour of Day", y: "Congestion Index"}
    )
    fig.update_layout(template="plotly_white", yaxis_tickformat=".0%")
    return fig


# -------------------------------------
# 2. Heatmap — weekday × hour
# -------------------------------------
def plot_heatmap(pvt: pd.DataFrame):
    """Plot congestion heatmap by weekday and hour."""
    fig = px.imshow(
        pvt,
        aspect="auto",
        color_continuous_scale="Inferno",
        labels=dict(color="Median congestion"),
        title="Congestion by Weekday × Hour (0=Mon)"
    )
    fig.update_layout(template="plotly_white")
    return fig


# -------------------------------------
# 3. Map — hotspots (optional for later)
# -------------------------------------
def map_hotspots(df_points: pd.DataFrame):
    """Plot congestion hotspots on an interactive map."""
    m = folium.Map(location=[43.6532, -79.3832], zoom_start=11)
    data = df_points[["latitude", "longitude", "congestion_index"]].dropna().values.tolist()
    HeatMap(data, radius=10, blur=18, max_zoom=13).add_to(m)
    return m

import pandas as pd
import geopandas as gpd
import folium

def choropleth_neighbourhoods(nh_geojson_path: str,
                              points_gdf: gpd.GeoDataFrame,
                              value_col: str = "congestion_index",
                              how: str = "median",
                              output_html: str = "data/processed/neighbourhood_congestion.html"):
    """
    Join point data to neighbourhood polygons, aggregate per neighbourhood,
    and render a Folium choropleth saved to HTML.
    """
    # load polygons and normalize name column -> 'neighbourhood'
    nh = gpd.read_file(nh_geojson_path).to_crs(4326)
    name_col = next((c for c in ["neighbourhood", "AREA_NAME", "NAME", "AREA_SHORT_CODE"] if c in nh.columns), None)
    if name_col != "neighbourhood":
        nh = nh.rename(columns={name_col: "neighbourhood"})

    # spatial join (project to meters for accurate geometry ops)
    pts3857, nh3857 = points_gdf.to_crs(3857), nh.to_crs(3857)
    joined = gpd.sjoin(pts3857, nh3857, how="left", predicate="within").to_crs(4326)

    # aggregate
    agg_series = (joined.groupby("neighbourhood")[value_col].median()
                  if how == "median" else joined.groupby("neighbourhood")[value_col].mean())
    nh_map = nh.merge(agg_series.rename("value"), on="neighbourhood", how="left")

    # render choropleth
    m = folium.Map(location=[43.6532, -79.3832], zoom_start=11)
    folium.Choropleth(
        geo_data=nh_map.to_json(),
        data=nh_map,
        columns=["neighbourhood", "value"],
        key_on="feature.properties.neighbourhood",
        fill_opacity=0.75,
        line_opacity=0.4,
        legend_name=f"{how.capitalize()} congestion index",
    ).add_to(m)

    m.save(output_html)
    return m