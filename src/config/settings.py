"""
Configuration settings for drought monitoring system.

Settings are loaded from environment variables (.env file) with pydantic validation.
"""

from pathlib import Path
from typing import Optional

from pydantic import Field, validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application configuration from environment variables."""

    # Project Info
    APP_NAME: str = "Vegetation Drought Resilience"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = False

    # OpenEO Backend Configuration
    OPENEO_BACKEND_URL: str = "https://openeo.creo.vito.be/openeo/1.1.0"
    OPENEO_BACKEND_NAME: str = "Vito"
    OPENEO_USERNAME: Optional[str] = "your-eodc-username"
    OPENEO_PASSWORD: Optional[str] = "your-eodc-password"
    OPENEO_SENTINEL2_COLLECTION_ID: str = "SENTINEL2_L2A"
    OPENEO_ERA5_COLLECTION_ID: str = "ERA5"
    OPENEO_AUTH_METHOD: str = "auto"
    OPENEO_CLIENT_ID: Optional[str] = None
    OPENEO_CLIENT_SECRET: Optional[str] = None
    OPENEO_AUTH_PROVIDER_ID: Optional[str] = None

    # Alternative backends for different data types
    OPENEO_SENTINEL2_BACKEND_URL: Optional[str] = None  # If different from main backend
    OPENEO_ERA5_BACKEND_URL: Optional[str] = None  # If different from main backend

    # PostgreSQL + PostGIS Database
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_USER: str = "drought_user"
    DB_PASSWORD: str = "your_secure_password"
    DB_NAME: str = "drought_database"
    DB_SSLMODE: str = "disable"

    @property
    def DB_CONNECTION_STRING(self) -> str:
        """PostgreSQL connection string for SQLAlchemy."""
        return (
            f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@"
            f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    # Region of Interest: Flanders, Belgium
    ROI_NAME: str = "flanders"
    ROI_NORTH: float = 51.507
    ROI_SOUTH: float = 50.674
    ROI_EAST: float = 5.918
    ROI_WEST: float = 2.754

    @property
    def ROI_BOUNDS(self) -> dict:
        """Return ROI bounding box as dict."""
        return {
            "north": self.ROI_NORTH,
            "south": self.ROI_SOUTH,
            "east": self.ROI_EAST,
            "west": self.ROI_WEST,
        }

    @property
    def ROI_BBOX_LIST(self) -> list:
        """Return ROI as [west, south, east, north] for OpenEO spatial_extent."""
        return [self.ROI_WEST, self.ROI_SOUTH, self.ROI_EAST, self.ROI_NORTH]

    # Data Directories
    DATA_DIR: Path = Field(default=Path("./data"))
    RAW_DATA_DIR: Path = Field(default=Path("./data/raw"))
    PROCESSED_DATA_DIR: Path = Field(default=Path("./data/processed"))
    REFERENCE_DATA_DIR: Path = Field(default=Path("./data/reference"))

    @validator("DATA_DIR", "RAW_DATA_DIR", "PROCESSED_DATA_DIR", "REFERENCE_DATA_DIR", pre=True)
    def ensure_path_exists(cls, v):
        """Create directories if they don't exist."""
        p = Path(v)
        p.mkdir(parents=True, exist_ok=True)
        return p

    # Feature Engineering
    BASELINE_START_YEAR: int = 2016
    BASELINE_END_YEAR: int = 2022
    TARGET_RESOLUTION_METERS: int = 100

    @property
    def BASELINE_YEARS(self) -> list:
        """List of baseline years."""
        return list(range(self.BASELINE_START_YEAR, self.BASELINE_END_YEAR + 1))

    # Drought Index Parameters
    DROUGHT_WINDOW_MONTHS: int = 1
    SPI_WEIGHT: float = 0.35
    VSI_WEIGHT: float = 0.35
    SM_WEIGHT: float = 0.30
    CONFIDENCE_THRESHOLD: float = 0.6

    @validator("SPI_WEIGHT", "VSI_WEIGHT", "SM_WEIGHT")
    def validate_weights(cls, v):
        """Weights must be between 0 and 1."""
        if not 0 <= v <= 1:
            raise ValueError("Weight must be between 0 and 1")
        return v

    # Land Cover Classes (ESA WorldCover or CORINE LC)
    LANDCOVER_CLASSES: dict = {
        "forest": {"lc_class": [10]},  # ESA: Dense forest
        "grassland": {"lc_class": [20, 30]},  # ESA: Herbaceous vegetation, shrubland
        "wetland": {"lc_class": [90]},  # ESA: Herbaceous wetland
        "agricultural": {"lc_class": [40]},  # ESA: Cultivated areas
    }

    # Sentinel-2 Parameters (via OpenEO)
    SENTINEL2_MAX_CLOUD_COVER: int = 20
    SENTINEL2_BANDS: list[str] = Field(
        default=[
            "B02",  # Blue (10m)
            "B03",  # Green (10m)
            "B04",  # Red (10m)
            "B05",  # Vegetation Red Edge (20m)
            "B06",  # Vegetation Red Edge (20m)
            "B07",  # Vegetation Red Edge (20m)
            "B08",  # NIR (10m)
            "B8A",  # Vegetation Red Edge (20m)
            "B11",  # SWIR (20m)
            "B12",  # SWIR (20m)
            "SCL",  # Scene Classification Layer (20m)
        ]
    )
    SENTINEL2_RESOLUTION: int = 10  # 10m native resolution

    # ERA5 Parameters
    ERA5_VARIABLES: list[str] = Field(
        default=[
            "temperature_2m",
            "total_precipitation_sum",
            "volumetric_soil_water_layer_1",
            "volumetric_soil_water_layer_2",
        ]
    )

    @validator("SENTINEL2_BANDS", "ERA5_VARIABLES", pre=True)
    def parse_list_from_env(cls, v):
        """Allow comma-separated env values for list fields."""
        if isinstance(v, str):
            return [item.strip() for item in v.split(",") if item.strip()]
        if isinstance(v, (list, tuple)):
            return list(v)
        return list(v)

    ERA5_RESOLUTION_METERS: int = 25000  # ~25 km

    # CDS API Configuration (for ERA5 data access)
    CDS_API_URL: str = "https://cds.climate.copernicus.eu/api/v2"
    CDS_API_KEY: Optional[str] = None  # Format: UID:API_KEY from CDS account
    ERA5_USE_CDSAPI: bool = False  # Use CDS API instead of OpenEO for ERA5

    # Drought Index Thresholds
    DROUGHT_SEVERITY_THRESHOLDS: dict = {
        "no_drought": {"range": [0.0, 0.2]},
        "mild": {"range": [0.2, 0.4]},
        "moderate": {"range": [0.4, 0.7]},
        "severe": {"range": [0.7, 1.0]},
    }

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: Path = Field(default=Path("logs/drought_monitoring.log"))

    @validator("LOG_FILE", pre=True)
    def ensure_logs_dir(cls, v):
        """Create logs directory if it doesn't exist."""
        p = Path(v)
        p.parent.mkdir(parents=True, exist_ok=True)
        return p

    # Streamlit Dashboard
    STREAMLIT_THEME: str = "light"
    STREAMLIT_MAP_CENTER_LAT: float = 51.1
    STREAMLIT_MAP_CENTER_LNG: float = 4.4
    STREAMLIT_MAP_ZOOM: int = 8

    class Config:
        """Pydantic config."""

        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        extra = "ignore"


# Global settings instance
_settings: Optional[Settings] = None


def get_settings() -> Settings:
    """Get or create singleton Settings instance."""
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings


# For convenience, expose common settings at module level
settings = get_settings()

# Aliases for common attributes
FLANDERS_BOUNDS = settings.ROI_BOUNDS
DB_CONNECTION_STRING = settings.DB_CONNECTION_STRING
BASELINE_YEARS = settings.BASELINE_YEARS
LANDCOVER_CLASSES = settings.LANDCOVER_CLASSES
