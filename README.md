---

## 🧠 How It Works

### 1️⃣ Data Source
- The main dataset used is:  
  **Traffic Volumes - Midblock Vehicle Speed, Volume and Classification Counts**
- This dataset includes vehicle counts, average speeds, and road segment coordinates.

### 2️⃣ Data Processing
- Loaded and cleaned using **pandas**  
- Aggregated hourly using `groupby()`  
- Spatially joined with Toronto neighborhood polygons using **GeoPandas**

### 3️⃣ Visualizations
- Hourly line plot of congestion levels  
- Weekday vs. Hour heatmap  
- Neighborhood-level congestion map (**Folium**)  

---

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
