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

You can download the full CSV directly from the City of Toronto Open Data site: https://open.toronto.ca/dataset/traffic-volumes-midblock-vehicle-speed-volume-and-classification-counts/

- **CSV:** Traffic Volumes & Vehicle Speeds
- **GeoJSON:** Toronto Neighbourhoods (Included in the raw folder) 

---

## ⚠️ Notes
- Large raw data files (CSV & GeoJSON) are not included in the repository due to GitHub's 25 MB file limit.
- Use the provided script or link in this README to download them directly.
- Generated HTML files are saved locally under `data/processed/`.

---

## 📊 Results

After analyzing over 1.2 million traffic speed records, I uncovered several key insights into Toronto's traffic congestion patterns:

### 1. Rush Hour Peaks (7–9 AM & 4–6 PM)
- Congestion was at its worst during typical commute times, with speeds often dropping below 25 km/h on major roads like Bloor Street, Yonge Street, and near the Gardiner Expressway entrances.
- The data clearly shows the classic "double-peak" pattern — one in the morning as people head downtown, and another in the evening as they travel home.

### 2. Weekday vs. Weekend Patterns
- Weekdays showed sharp congestion spikes during morning and evening commutes.
- Weekends, on the other hand, had smoother overall flow, with only slight slowdowns around midday (12 PM–2 PM) — likely from shopping and leisure trips.

### 3. Neighbourhood Differences
- Central areas like Downtown, Waterfront, and Midtown experienced the heaviest congestion, while Etobicoke, Scarborough, and North York maintained faster speeds (often 40 km/h or higher).
- The choropleth maps made these differences easy to visualize, highlighting Toronto's downtown bottleneck problem.

### 4. Off-Peak Stability
- Late-night and early-morning traffic (roughly 10 PM–5 AM) was much smoother, with median speeds ranging from 45–55 km/h.

**Overall:** The project revealed that Toronto's traffic congestion isn't evenly spread out — it's concentrated in the downtown core and during predictable rush hours. These findings suggest that policies like flexible work hours or better public transit coverage could meaningfully reduce peak-hour congestion.

---
