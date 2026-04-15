# vegetation_drought_resilience

A modular Python tool for **drought impact monitoring** using satellite imagery (Sentinel-2) and weather data (ERA5). Detects drought-affected areas in Flanders, Belgium, using a scientifically-grounded multi-component drought index.

## Overview

This project combines:
- **Satellite data**: Sentinel-2 imagery (10m resolution) via OpenEO (Copernicus Data Space)
- **Weather data**: ERA5 daily climate variables (precipitation, temperature, soil moisture)
- **Land cover data**: ESA WorldCover for natural area filtering (forests, grasslands, wetlands)
- **Drought detection**: Percentile-based multi-component index (SPI, VSI, soil moisture anomalies)
- **Interactive visualization**: Folium maps + Streamlit dashboard for exploration and analysis

## Features

✅ **Data Ingestion**: Automated download of Sentinel-2 and ERA5 data via OpenEO  
✅ **Preprocessing**: Cloud masking, land cover filtering, spatial alignment to 100m grid  
✅ **Feature Engineering**: NDVI/NDWI vegetation indices, precipitation & temperature anomalies, soil moisture percentiles  
✅ **Scientific Drought Index**: Composite index combining:
  - **SPI** (Standardized Precipitation Index) — WMO standard
  - **VSI** (Vegetation Stress Index) — remote sensing standard
  - **Soil Moisture Percentile** — direct drought signal
✅ **Geospatial Database**: PostGIS for efficient spatial queries and historical tracking  
✅ **Interactive Dashboard**: Streamlit app with drought map, filters, and time-series analysis  

## Quick Start

### Prerequisites

- Python 3.10+
- PostgreSQL with PostGIS extension
- OpenEO backend account (free: https://dataspace.copernicus.eu for CDSE backend)

### Installation

1. **Clone repository**
   ```bash
   git clone https://github.com/yourusername/vegetation_drought_resilience.git
   cd vegetation_drought_resilience
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\Activate.ps1
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   # Or for development:
   pip install -e ".[dev]"
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your credentials:
   # - OPENEO_BACKEND_URL, OPENEO_USERNAME, OPENEO_PASSWORD
   # - DB_HOST, DB_USER, DB_PASSWORD
   ```

5. **Verify OpenEO backend connection**
   ```bash
   python -c "import openeo; conn = openeo.connect('https://openeo.dataspace.copernicus.eu/openeo/1.1.0'); print(conn)"
   ```

6. **Initialize PostGIS database**
   ```bash
   psql -h localhost -U postgres
   CREATE DATABASE drought_database;
   \c drought_database
   CREATE EXTENSION PostGIS;
   \q
   ```

### Running the Dashboard

```bash
streamlit run app/main.py
```

Then open `http://localhost:8501` in your browser.

## Project Structure

```
src/
  ├── config/              # Settings and configuration
  ├── data/                # Data fetching & database
  ├── preprocessing/       # Cloud masking, land cover filtering
  ├── features/            # Vegetation indices, anomalies, baselines
  ├── modeling/            # Drought index computation
  ├── visualization/       # Maps and charts
  └── utils/               # Logging, validation

app/                        # Streamlit dashboard
  ├── pages/               # Dashboard pages
  └── components/          # Reusable Streamlit components

tests/                      # Unit and integration tests

docs/                       # Documentation
```

## Drought Detection Method

### Percentile-Based Multi-Component Index (PMDI)

The tool computes drought severity using three complementary indices:

| Index | Data Source | Scale | Interpretation |
|-------|-------------|-------|-----------------|
| **SPI** | ERA5 precipitation | [-3, +3] | SPI < -1 = dry; < -2 = severe drought (WMO standard) |
| **VSI** | Sentinel-2 NDVI | [0, 1] | VSI > 0.3 = visible vegetation stress |
| **SM %ile** | ERA5-Land soil moisture | [0, 1] | 0 = very wet; 1 = very dry (relative to 2016–2022 history) |

**Composite Index**: CDI = median(rank(SPI), rank(VSI), rank(SM_pct))

**Drought Classification** (adaptive percentiles in Flanders):
- No drought: CDI < 20th percentile (normal conditions)
- Mild: 20–40th percentile
- Moderate: 40–70th percentile
- Severe: > 70th percentile

See [docs/architecture.md](docs/architecture.md) for detailed methodology.

## Development Status

**Status**: 🔨 Early Alpha (Phase 1: Project Setup)

This is the initial project setup phase. Core modules and the Streamlit dashboard are being implemented.

---

**Last Updated**: April 2024