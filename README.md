# 🛣️ Toronto Traffic Congestion Analyzer
**Language:** Python  
**Libraries:** `pandas`, `plotly`, `geopandas`, `folium`, `requests`

---

## Overview
The **Toronto Traffic Congestion Analyzer** uses real open data from the [City of Toronto Open Data Portal](https://open.toronto.ca) to visualize and analyze **traffic speed, volume, and congestion** patterns across the city.

It helps identify:
- Which hours of the day experience the worst traffic congestion  
- How congestion varies between weekdays and weekends  
- Which Toronto neighborhoods experience the highest congestion  

## 🗺️ Example Outputs
| Visualization | Description |
|----------------|-------------|
| 🕒 Hourly Congestion Chart | Shows how congestion changes throughout the day. |
| 📆 Heatmap (Weekday × Hour) | Displays patterns across the week. |
| 🗺️ Neighborhood Choropleth | Highlights which Toronto neighborhoods are most congested. |

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the repository

```bash
git clone https://github.com/cflau31666/toronto-traffic-congestion-analyzer.git
cd toronto-traffic-congestion-analyzer
```

---

### 2️⃣ Install dependencies

```bash
pip install pandas plotly geopandas folium
```

---

### 3️⃣ Fetch the dataset

You can download the full CSV directly from the City of Toronto Open Data site : https://open.toronto.ca/dataset/traffic-volumes-midblock-vehicle-speed-volume-and-classification-counts/
- **CSV:** Traffic Volumes & Vehicle Speeds
- **GeoJSON:** Toronto Neighbourhoods (Included in the raw folder) 

---

## ⚠️ Notes
- Large raw data files (CSV & GeoJSON) are not included in the repository due to GitHub's 25 MB file limit.
- Use the provided script or link in this README to download them directly.
- Generated HTML files are saved locally under `data/processed/`.

---
