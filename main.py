import os
import pandas as pd

from src.transform import (
    compute_avg_speed,
    add_time_features,
    build_congestion_index,
    to_geodf,
)
from src.aggregate import hourly_average, weekday_hour_heatmap
from src.viz import (
    plot_hourly_line,
    plot_heatmap,
    choropleth_neighbourhoods,
    map_hotspots,
)

CSV_PATH = "data/raw/svc_raw_data_speed_2020_2024.csv"
NH_PATH  = "data/raw/Neighbourhoods - 4326.geojson"
OUT_DIR  = "data/processed"
CHORO_HTML = os.path.join(OUT_DIR, "neighbourhood_congestion.html")
HOTSPOTS_HTML = os.path.join(OUT_DIR, "hotspots.html")


def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    # 1) Load + transform
    df = pd.read_csv(CSV_PATH, low_memory=False, on_bad_lines="skip")
    df = compute_avg_speed(df)            # adds: speed_kmh, total_volume
    df = add_time_features(df)            # adds: local_ts, hour, dow, date
    df = build_congestion_index(df, speed_col="speed_kmh")

    # 2) Quality filter (tune as you like)
    df = df[(df["speed_kmh"].between(5, 120)) & (df["total_volume"] >= 3)].copy()
    df = df.dropna(subset=["latitude", "longitude", "congestion_index"])

    # 3) Citywide visuals
    hourly = hourly_average(df, value_col="congestion_index")
    fig1 = plot_hourly_line(hourly, y="congestion_index")
    fig1.update_layout(title="Median Congestion by Hour (Citywide)")
    fig1.show()

    heat = weekday_hour_heatmap(df, value_col="congestion_index")
    fig2 = plot_heatmap(heat)
    fig2.show()

    # 4) Geographic outputs
    # 4a) Choropleth by neighbourhood (uses points_gdf inside)
    gpoints = to_geodf(df)  # GeoDataFrame of points from lon/lat
    choropleth_neighbourhoods(
        nh_geojson_path=NH_PATH,
        points_gdf=gpoints,
        value_col="congestion_index",
        how="median",
        output_html=CHORO_HTML,
    )
    print(f"Saved → {CHORO_HTML}")

    # 4b) Hotspots heat map (point intensity)
    loc = (df.groupby(["count_id", "location_name", "latitude", "longitude"], as_index=False)
             ["congestion_index"].median().dropna())
    m_hot = map_hotspots(loc)
    m_hot.save(HOTSPOTS_HTML)
    print(f"Saved → {HOTSPOTS_HTML}")

    # ------------------------------------------------
    # 5) Optional: Time-of-day congestion maps
    # ------------------------------------------------
    print("Generating time-of-day congestion maps...")

    # Morning rush (6–10 AM)
    morning = df[df["hour"].between(6, 10)]
    choropleth_neighbourhoods(
        NH_PATH,
        to_geodf(morning),
        value_col="congestion_index",
        how="median",
        output_html="data/processed/morning_congestion.html"
    )

    # Evening rush (4–8 PM)
    evening = df[df["hour"].between(16, 20)]
    choropleth_neighbourhoods(
        NH_PATH,
        to_geodf(evening),
        value_col="congestion_index",
        how="median",
        output_html="data/processed/evening_congestion.html"
    )

    # Overnight (0–4 AM)
    overnight = df[df["hour"].between(0, 4)]
    choropleth_neighbourhoods(
        NH_PATH,
        to_geodf(overnight),
        value_col="congestion_index",
        how="median",
        output_html="data/processed/overnight_congestion.html"
    )

    print("Saved → morning, evening, and overnight congestion maps.")




if __name__ == "__main__":
    main()