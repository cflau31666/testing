"""Data aggregation module."""
import pandas as pd

def hourly_average(df: pd.DataFrame, value_col: str = "speed_kmh") -> pd.DataFrame:
    """Compute median metric per hour."""
    return df.groupby("hour", as_index=False)[value_col].median()

def weekday_hour_heatmap(df, value_col="congestion_index"):
    pvt = df.pivot_table(index="dow", columns="hour", values=value_col, aggfunc="median")
    return pvt.sort_index()

def neighbourhood_summary(df: pd.DataFrame, value_col="congestion_index") -> pd.DataFrame:
    # df can be GeoDataFrame from the spatial join
    return (df.dropna(subset=["neighbourhood"])
              .groupby("neighbourhood", as_index=False)[value_col]
              .median())