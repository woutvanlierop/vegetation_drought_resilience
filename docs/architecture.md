# Drought Impact Monitoring - Architecture & Design

## System Overview

The vegetation_drought_resilience project is a modular Python application for detecting and visualizing drought impacts using satellite imagery (Sentinel-2) and weather data (ERA5).

### High-Level Data Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                     DATA SOURCES                                 │
├─────────────────────────────────────────────────────────────────┤
│ OpenEO (Copernicus Data Space Ecosystem)                         │
│  ├─ Sentinel-2 (10m, 5-day revisit)                            │
│  ├─ ERA5 daily weather (31km, temperature, precip, soil water) │
│  └─ ESA WorldCover land classification (10m)                    │
└────────┬────────────────────────────────────────────────────────┘
         │
         ├──→ src/data/fetchers.py       [Phase 2: OpenEO API calls]
         │
┌────────▼────────────────────────────────────────────────────────┐
│                  DATA FETCHING & STORAGE                         │
├──────────────────────────────────────────────────────────────────┤
│ - Download Sentinel-2 scenes (NetCDF/GeoTIFF)                   │
│ - Download ERA5 daily data (NetCDF)                             │
│ - Cache locally in data/raw/                                    │
│ - Store metadata in PostGIS (raw_sentinel_scenes table)         │
└────────┬────────────────────────────────────────────────────────┘
         │
         ├──→ src/preprocessing/          [Phase 3: Cloud masking]
         │    ├─ cloud_masking.py         [Remove cloudy pixels]
         │    ├─ land_cover.py            [Filter natural areas only]
         │    └─ alignment.py             [Resample to 100m grid]
         │
┌────────▼────────────────────────────────────────────────────────┐
│              PREPROCESSING & ALIGNMENT                           │
├──────────────────────────────────────────────────────────────────┤
│ Sentinel-2:                                                      │
│  1. Apply QA60 cloud mask (bits 10, 11)                         │
│  2. Filter by land cover: forest, grassland, wetland            │
│  3. Resample 10m → 100m using nearest neighbor                  │
│                                                                  │
│ ERA5:                                                            │
│  1. Resample 25km → 100m using bilinear interp                 │
│  2. Align to Sentinel-2 dates                                   │
└────────┬────────────────────────────────────────────────────────┘
         │
         ├──→ src/features/               [Phase 4: Feature eng]
         │    ├─ vegetation.py            [NDVI, NDWI, EVI]
         │    ├─ weather.py               [SPI, temp/precip anom]
         │    └─ baseline.py              [Historical baseline]
         │
┌────────▼────────────────────────────────────────────────────────┐
│         FEATURE EXTRACTION & BASELINE                            │
├──────────────────────────────────────────────────────────────────┤
│ NDVI = (B8 - B4) / (B8 + B4)                                    │
│ SPI = (Precip - Mean(2016-2022)) / Std(2016-2022)             │
│ VSI = 1 - (NDVI_current / NDVI_baseline_p50)                   │
│ SM_pct = percentile_rank(SM_current in historical_dist)        │
│                                                                  │
│ Load/compute baselines from 2016-2022 archive                  │
└────────┬────────────────────────────────────────────────────────┘
         │
         ├──→ src/modeling/               [Phase 5: Index calc]
         │    └─ drought_index.py         [Composite index]
         │
┌────────▼────────────────────────────────────────────────────────┐
│          DROUGHT DETECTION (PMDI)                               │
├──────────────────────────────────────────────────────────────────┤
│ 1. Compute SPI [-3, +3]                                         │
│ 2. Compute VSI [0, 1] (vegetation stress)                       │
│ 3. Compute SM Percentile [0, 1] (soil dryness)                 │
│                                                                  │
│ 4. Composite Drought Index (CDI):                               │
│    CDI = median(rank(SPI), rank(VSI), rank(SM_pct))            │
│                                                                  │
│ 5. Classify by percentile (adaptive regional thresholds):       │
│    - No drought: CDI < 20th %ile                                │
│    - Mild: 20-40th %ile                                         │
│    - Moderate: 40-70th %ile                                     │
│    - Severe: > 70th %ile                                        │
│                                                                  │
│ 6. Confidence score: component agreement (0-1)                  │
└────────┬────────────────────────────────────────────────────────┘
         │
         ├──→ src/data/database.py        [Phase 6: PostGIS]
         │
┌────────▼────────────────────────────────────────────────────────┐
│           SPATIAL DATABASE (PostGIS)                             │
├──────────────────────────────────────────────────────────────────┤
│ Tables:                                                          │
│  - processed_drought_index                                       │
│    (date, geometry, CDI, severity, SPI, VSI, SM_pct, conf)     │
│  - baseline_stats (historical stats per month per index)       │
│  - raw_sentinel_scenes (metadata)                               │
│                                                                  │
│ Enables spatial queries & historical tracking                   │
└────────┬────────────────────────────────────────────────────────┘
         │
         ├──→ src/visualization/          [Phase 7: Viz]
         │    └─ maps.py                  [Folium maps]
         │
┌────────▼────────────────────────────────────────────────────────┐
│             VISUALIZATION LAYER                                  │
├──────────────────────────────────────────────────────────────────┤
│ Folium maps:                                                     │
│  - Interactive drought severity map (color ramp)                │
│  - Overlay: region boundaries, land cover classes               │
│  - Exported to HTML for static sharing                          │
│                                                                  │
│ Static plots:                                                    │
│  - Time series (NDVI, SPI, CDI for sample regions)             │
│  - Severity distributions                                       │
│  - Regional comparisons                                         │
└────────┬────────────────────────────────────────────────────────┘
         │
         ├──→ app/main.py                 [Phase 8: Dashboard]
         │
┌────────▼────────────────────────────────────────────────────────┐
│           STREAMLIT DASHBOARD                                   │
├──────────────────────────────────────────────────────────────────┤
│ Main page:                                                       │
│   - Drought map (Folium embed)                                  │
│   - Sidebar filters: land cover, severity, date range          │
│   - Summary statistics table                                    │
│                                                                  │
│ Analysis page:                                                   │
│   - Time series for selected region                             │
│   - Component breakdown (SPI, VSI, SM)                          │
│                                                                  │
│ Data explorer page:                                              │
│   - Raw data inspection                                         │
│   - Debug tables                                                │
└────────▼────────────────────────────────────────────────────────┘
           ↓
        📊 INTERACTIVE DASHBOARD (localhost:8501)
```

---

## Module Responsibilities

### `src/config/`
- **settings.py**: Centralized configuration (OpenEO credentials, DB connection, ROI bounds, parameters)
- Load from `.env` file via pydantic

### `src/data/`
- **fetchers.py**: OpenEO API calls for Sentinel-2 and ERA5 data
- **database.py**: PostGIS database operations (schema, CRUD, queries)

### `src/preprocessing/`
- **cloud_masking.py**: QA band processing, cloud/shadow filters
- **land_cover.py**: ESA WorldCover filtering (forest, grassland, wetland)
- **alignment.py**: Resampling to 100m, spatial/temporal alignment

### `src/features/`
- **vegetation.py**: NDVI, NDWI, EVI computation from Sentinel-2
- **weather.py**: SPI, temperature/precipitation anomalies from ERA5
- **baseline.py**: Historical baseline computation and caching (2016-2022)

### `src/modeling/`
- **drought_index.py**: Percentile-Based Multi-Component Index (PMDI)
  - Composes SPI, VSI, soil moisture into CDI
  - Classifies severity by regional percentiles
  - Computes confidence scores

### `src/visualization/`
- **maps.py**: Folium interactive maps
- **plotting.py**: Static MatplotlibSeaborn charts

### `src/utils/`
- **logging_config.py**: Loguru logging setup
- **validators.py**: Input validation (dates, bbox, rasters)

### `app/`
- **main.py**: Streamlit entry point
- **pages/**: Multi-page dashboard (dashboard, analysis, data_explorer)
- **components/**: Reusable Streamlit filters and charts

### `tests/`
- Unit tests for each module
- Integration tests (full pipeline)
- Fixtures in conftest.py

---

## Technology Stack

| Component | Technology | Why |
|-----------|-----------|-----|
| Data fetching | OpenEO API | Transparent data access, flexible backend selection (CDSE/EODC/SentinelHub) |
| Satellite data | Sentinel-2 L2A (10m) | Free, EU-focused, high quality |
| Weather data | ERA5 daily (31km) | Comprehensive, 40+ variables |
| Geospatial processing | rasterio, geopandas, xarray | Standard tools, NumPy-compatible |
| Database | PostgreSQL + PostGIS | Spatial queries, multi-user, open-source |
| Visualization | Folium + Matplotlib | Interactive + static maps |
| Dashboard | Streamlit | Fast iteration, zero frontend code |
| Testing | pytest | Standard Python testing framework |

---

## Key Design Decisions

### 1. Percentile-Based Fusion (not weighted average)
- **Why**: Avoids arbitrary weight tuning, each component equally important
- **How**: Rank SPI, VSI, SM_pct separately → median of ranks → CDI
- **Benefit**: Transparent, defensible, no hyper-parameter tuning

### 2. 100m Target Resolution
- **Why**: Balance between Sentinel-2 (10m) detail and ERA5 (25km) coarseness
- **How**: Resample Sentinel-2 down, ERA5 up to 100m grid
- **Trade-off**: Loses fine detail but manageable file sizes & computation

### 3. Monthly Aggregation
- **Why**: Aligns with climate data, appropriate timescale for drought
- **How**: Use medians/percentiles over 7–10 day windows, aggregate to monthly
- **Benefit**: Reduces cloud cover impact, cleaner signal

### 4. Adaptive Regional Thresholds
- **Why**: Percentile thresholds adapt to regional baseline (coastal vs. inland)
- **How**: Compute CDI distribution in Flanders, use 20th/40th/70th percentiles
- **Benefit**: "Severe" in Flanders differs from globally (regional relevance)

### 5. PostGIS Database (not just files)
- **Why**: Multi-user access, spatial queries, version history
- **How**: Store processed results normalized (date, geometry, metrics)
- **Benefit**: Scale to multiple regions, months; efficient queries

---

## Phase-by-Phase Implementation (2-week MVP)

| Phase | Deliverable | Duration |
|-------|-------------|----------|
| 1 | Project structure, config, dependencies | 1 day ✅ |
| 2 | Data fetching (OpenEO Sentinel-2 + ERA5) | 2 days |
| 3 | Preprocessing (cloud mask, land cover, alignment) | 3 days |
| 4 | Features (NDVI, SPI, VSI, baselines) | 2 days |
| 5 | Drought index (PMDI) | 1 day |
| 6 | PostGIS storage | 2 days |
| 7 | Visualization (maps, plots) | 2 days |
| 8 | Streamlit dashboard | 3 days |
| 9 | Testing + docs | 2 days |
| 10 | Polish + handoff | 1 day |

**Total: ~2 weeks** (aggressive, can extend to 3 weeks)

---

## Running the Project

### First Time Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Create .env from template
cp .env.example .env
# Edit .env: OpenEO credentials, DB connection, etc.

# Verify OpenEO backend connection
python -c "import openeo; conn = openeo.connect('https://openeo.dataspace.copernicus.eu/openeo/1.1.0'); print(conn)"

# Initialize PostGIS database
psql -c "CREATE DATABASE drought_database;"
psql drought_database -c "CREATE EXTENSION PostGIS;"

# Initialize package (editable install)
pip install -e .
```

### Running Pipeline
```bash
# Install package in development mode
pip install -e .

# Fetch data for July 2023 (Phase 2)
vegetation-drought-resilience fetch-data 2023-07-01 2023-07-31

# Or run directly with Python
python -m src.cli fetch-data 2023-07-01 2023-07-31

# Launch dashboard
streamlit run app/main.py
```

---

## Next Steps (Post-MVP)

- Multi-month data (expand to 1 year)
- Date range picker in dashboard
- Regional forecasting (1–3 month ahead using ML)
- Sub-index weighting tuning (expert elicitation)
- Add more vegetation indices (EVI, MSAVI)
- Integrate soil moisture satellite data (SMOS)
- Deploy to cloud (Streamlit Cloud, AWS EC2, GCP)

---

**Status**: 🔨 Phase 1 Complete (Project Setup)  
**Next**: Phase 2 (Data Fetching)
