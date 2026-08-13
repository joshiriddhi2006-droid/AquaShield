# 🚨 AquaShield — Vehicle-Aware Flood Navigation & GIS System

> **An intelligent, real-time spatial navigation and urban decision-support platform designed to reroute commuters during severe urban flooding based on vehicle water-wading thresholds.**

---

## 📌 Project Overview
During heavy monsoon rains and flash floods, static navigation systems (like standard maps) often guide commuters through waterlogged underpasses and submerged roads. **AquaShield** solves this by dynamically calculating risk based on **vehicle ground clearance & water depth capacity**. 

Whether you are riding a two-wheeler, driving a sedan, navigating an SUV, or operating an emergency ambulance, AquaShield provides tailored safe corridors in real-time.

---

## 🌟 Key Features

* 🚘 **Vehicle Water-Clearance Assessment:** Dynamic route safety thresholding for:
  * 🛵 **Two-Wheelers** (*Max 10 cm clearance*)
  * 🚗 **Sedans / Hatchbacks** (*Max 15 cm clearance*)
  * 🚙 **SUVs / Off-Roaders** (*Max 32 cm clearance*)
  * 🚨 **Emergency Vehicles & Ambulances** (*Green Corridor Overrides up to 50 cm*)
* 🗺️ **Dual-Engine Interactive GIS Map:** High-definition Hybrid Satellite and OpenStreetMap rendering with live GPS tracking and dynamic hazard radii plotting.
* 📸 **Visual Incident Inspector:** Image-based spatial verification system to simulate flood levels and plot verified hazard points on the GIS map.
* 📊 **City Analytics Dashboard:** Interactive spatial risk distribution and department-wise complaint tracking powered by Plotly charts.
* 💬 **AquaBot Incident Assistant:** Interactive emergency assistance interface with dispatch ID integration (`AMB-108`, `FIRE-101`).

---

## 🛠️ Tech Stack & Tools

* **Frontend & Web Framework:** Streamlit
* **GIS & Spatial Mapping:** Folium, Streamlit-Folium
* **Data Engine & Processing:** Pandas
* **Data Visualization:** Plotly Express
* **Programming Language:** Python 3.10+

---

## 🚀 Local Installation & Setup

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/aquashield-flood-gis.git
   cd aquashield-flood-gis