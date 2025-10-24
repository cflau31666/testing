import pandas as pd
import numpy as np
import geopandas as gpd

def to_geodf(df: pd.DataFrame) -> gpd.GeoDataFrame:
    return gpd.GeoDataFrame(
        df,
        geometry=gpd.points_from_xy(df["longitude"], df["latitude"]),
        crs="EPSG:4326",
    )

def join_neighbourhoods(points_gdf: gpd.GeoDataFrame, nh_gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    # project for accurate spatial join, then return to 4326
    pts = points_gdf.to_crs(3857)
    polys = nh_gdf.to_crs(3857)
    joined = gpd.sjoin(pts, polys, how="left", predicate="within").to_crs(4326)
    return joined

def compute_avg_speed(df: pd.DataFrame) -> pd.DataFrame:
    vol_cols = [c for c in df.columns if c.startswith("vol_")]

    bin_midpoints = []
    for c in vol_cols:
        lo, hi = c.replace("vol_", "").replace("kph", "").split("_")
        bin_midpoints.append((int(lo) + int(hi)) / 2)

    vol_values = df[vol_cols].values
    df["total_volume"] = vol_values.sum(axis=1)

    weighted = (vol_values * bin_midpoints).sum(axis=1)
    df["speed_kmh"] = np.divide(
        weighted, df["total_volume"],
        out=np.zeros_like(df["total_volume"], dtype=float),
        where=df["total_volume"] > 0
    )
    # drop bins with no vehicles (optional but helpful)
    df = df[df["total_volume"] > 0].copy()
    return df

LOCAL_TZ = "America/Toronto"

def add_time_features(df: pd.DataFrame) -> pd.DataFrame:
    # Many open-data timestamps are ISO strings; coerce just in case.
    ts = pd.to_datetime(df["time_start"], errors="coerce", utc=True)
    # If times are already local-naive, use: ts = pd.to_datetime(df["time_start"]).dt.tz_localize(LOCAL_TZ)
    df["local_ts"] = ts.dt.tz_convert(LOCAL_TZ)
    df["hour"] = df["local_ts"].dt.hour
    df["dow"]  = df["local_ts"].dt.dayofweek  # 0=Mon
    df["date"] = df["local_ts"].dt.date
    return df

def build_congestion_index(df: pd.DataFrame, speed_col="speed_kmh") -> pd.DataFrame:
    # Per-location free-flow: median speed 2–4am
    base = (df[(df["hour"]>=2) & (df["hour"]<4)]
              .groupby("count_id")[speed_col].median()
              .rename("freeflow_speed"))
    df = df.join(base, on="count_id")
    # Fallback: if some locations lack 2–4am data, use global overnight median
    global_ff = (df[(df["hour"]>=2) & (df["hour"]<4)][speed_col].median())
    df["freeflow_speed"] = df["freeflow_speed"].fillna(global_ff)

    df["congestion_index"] = 1 - (df[speed_col] / df["freeflow_speed"])
    df["congestion_index"] = df["congestion_index"].clip(0, 1)
    return df