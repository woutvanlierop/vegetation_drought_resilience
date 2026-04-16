"""
OpenEO data fetchers for Sentinel-2 and ERA5 weather data via Copernicus.

This module handles all data download operations from OpenEO backends.
Supports multiple backends:
- EODC (https://openeo.creo.vito.be) — European Open Data Cube
- CDSE (https://openeo.dataspace.copernicus.eu) — Copernicus Data Space Ecosystem (free)
- Sentinel Hub
- CDS API (https://cds.climate.copernicus.eu) — Copernicus Climate Data Store for ERA5
"""

import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Tuple

import cdsapi
import openeo
import xarray as xr
from loguru import logger


def authenticate_openeo(
    backend_url: str,
    client_id: Optional[str] = None,
    client_secret: Optional[str] = None,
    provider_id: Optional[str] = None
) -> openeo.Connection:
    """
    Authenticate with OpenEO backend.

    Args:
        backend_url: OpenEO backend URL (e.g., https://openeo.creo.vito.be/openeo/1.1.0)
        username: OpenEO username
        password: OpenEO password
        client_id: OpenEO OIDC client ID
        client_secret: OpenEO OIDC client secret
        provider_id: OpenEO OIDC provider ID
        auth_method: Authentication method to use (basic, client_credentials, resource_owner, auto)

    Returns:
        Authenticated openeo.Connection object

    Raises:
        Exception: If authentication fails
    """
    connection = openeo.connect(backend_url)
    try:
        connection.authenticate_oidc_client_credentials(
                client_id=client_id,
                client_secret=client_secret,
                provider_id=provider_id,
            )
        logger.info("Authenticated with OpenEO backend: {}", backend_url)
        return connection
    except Exception as e:
        logger.error(f"Failed to authenticate with OpenEO: {e}")
        raise


def _build_spatial_extent(roi: list) -> dict:
    """Build an OpenEO-compatible spatial extent from ROI bounds."""
    if len(roi) != 4:
        raise ValueError("ROI must be [west, south, east, north]")
    return {"west": roi[0], "south": roi[1], "east": roi[2], "north": roi[3]}


def _normalize_band_list(bands: Optional[list]) -> Optional[list]:
    """Normalize band or variable lists for OpenEO load_collection."""
    if bands is None:
        return None

    legacy_band_map = {
        "B2": "B02",
        "B3": "B03",
        "B4": "B04",
        "B5": "B05",
        "B6": "B06",
        "B7": "B07",
        "B8": "B08",
        "B8A": "B8A",
        "B11": "B11",
        "B12": "B12",
        "SCL": "SCL",
    }

    normalized = []
    for band in bands:
        if not isinstance(band, str):
            continue
        band_name = band.strip().upper()
        normalized.append(legacy_band_map.get(band_name, band_name))

    return normalized


def fetch_sentinel2(
    backend_url: str,
    client_id: Optional[str],
    client_secret: Optional[str],
    provider_id: Optional[str],
    auth_method: str,
    roi: list,
    start_date: str,
    end_date: str,
    max_cloud_cover: int = 20,
    bands: Optional[list] = None,
    collection_id: str = "SENTINEL2_L2A",
) -> openeo.DataCube:
    """
    Fetch Sentinel-2 imagery from an OpenEO backend.

    Args:
        backend_url: OpenEO backend URL
        username: OpenEO username
        password: OpenEO password
        roi: Region of interest as [west, south, east, north]
        start_date: Start date in 'YYYY-MM-DD' format
        end_date: End date in 'YYYY-MM-DD' format
        max_cloud_cover: Maximum allowed cloud cover percentage (default 20)
        bands: List of band names to select (default: None / all available)
        collection_id: OpenEO collection identifier for Sentinel-2 data

    Returns:
        openeo.DataCube with Sentinel-2 scenes
    """
    connection = authenticate_openeo(
        backend_url=backend_url,
        client_id=client_id,
        client_secret=client_secret,
        provider_id=provider_id)
    spatial_extent = _build_spatial_extent(roi)
    selected_bands = _normalize_band_list(bands)

    try:
        cube = connection.load_collection(
            collection_id=collection_id,
            spatial_extent=spatial_extent,
            temporal_extent=[start_date, end_date],
            bands=selected_bands,
            max_cloud_cover=max_cloud_cover,
        )
        logger.info(
            "Loaded Sentinel-2 collection {} for {} to {}",
            collection_id,
            start_date,
            end_date,
        )
        return cube
    except Exception as e:
        logger.error("Failed to load Sentinel-2 collection {}: {}", collection_id, e)
        raise


def fetch_era5_daily(
    backend_url: str,
    client_id: Optional[str],
    client_secret: Optional[str],
    provider_id: Optional[str],
    auth_method: str,
    roi: list,
    start_date: str,
    end_date: str,
    variables: Optional[list] = None,
    collection_id: str = "ERA5",
) -> openeo.DataCube:
    """
    Fetch ERA5 daily weather data from an OpenEO backend.

    Args:
        backend_url: OpenEO backend URL
        username: OpenEO username
        password: OpenEO password
        roi: Region of interest as [west, south, east, north]
        start_date: Start date in 'YYYY-MM-DD' format
        end_date: End date in 'YYYY-MM-DD' format
        variables: List of variable names to fetch
            (e.g., 'temperature_2m', 'total_precipitation_sum')
        collection_id: OpenEO collection identifier for ERA5 climate data

    Returns:
        openeo.DataCube with ERA5 daily climate variables
    """
    connection = authenticate_openeo(
        backend_url=backend_url,
        client_id=client_id,
        client_secret=client_secret,
        provider_id=provider_id,
    )
    spatial_extent = _build_spatial_extent(roi)
    selected_variables = _normalize_band_list(variables)

    try:
        cube = connection.load_collection(
            collection_id=collection_id,
            spatial_extent=spatial_extent,
            temporal_extent=[start_date, end_date],
            bands=selected_variables,
        )
        logger.info(
            "Loaded ERA5 collection {} for {} to {}",
            collection_id,
            start_date,
            end_date,
        )
        return cube
    except Exception as e:
        logger.error("Failed to load ERA5 collection {}: {}", collection_id, e)
        raise


def download_to_netcdf(
    datacube: openeo.DataCube,
    output_file: str,
    format: str = "netcdf",
    max_retries: int = 3,
) -> str:
    """
    Download OpenEO DataCube to a local file.

    Args:
        datacube: openeo.DataCube to download
        output_file: Output file path
        format: Output format ('netcdf', 'GeoTIFF', 'COG', etc.)
        max_retries: Number of retry attempts for transient backend errors

    Returns:
        Path to downloaded file
    """
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    transient_codes = {"502", "503", "504"}

    for attempt in range(1, max_retries + 1):
        try:
            datacube.download(outputfile=output_path, format=format)
            logger.info("Downloaded OpenEO result to {}", output_path)
            return str(output_path)
        except Exception as e:
            error_text = str(e)
            if attempt < max_retries and any(code in error_text for code in transient_codes):
                logger.warning(
                    "Transient OpenEO error on attempt {}/{}: {}. Retrying...",
                    attempt,
                    max_retries,
                    e,
                )
                time.sleep(2 ** (attempt - 1))
                continue

            logger.error(
                "Failed to download OpenEO result to {} with format {}: {}",
                output_path,
                format,
                e,
            )
            raise
    raise RuntimeError(f"Exceeded maximum retries ({max_retries}) for downloading OpenEO result to {output_path}")


def download_to_geotiff(
    datacube: openeo.DataCube,
    output_file: str,
) -> str:
    """
    Download OpenEO DataCube to Cloud Optimized GeoTIFF (COG).

    Args:
        datacube: openeo.DataCube to download
        output_file: Output file path

    Returns:
        Path to downloaded file
    """
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        datacube.download(outputfile=output_path, format="COG")
        logger.info("Downloaded OpenEO result to {}", output_path)
        return str(output_path)
    except Exception as e:
        logger.error("Failed to download OpenEO COG to {}: {}", output_path, e)
        raise


def fetch_era5_cds_api(
    api_url: str,
    api_key: str,
    roi: list,
    start_date: str,
    end_date: str,
    variables: Optional[list] = None,
    output_file: str = "era5.nc",
) -> str:
    """
    Fetch ERA5 data from Copernicus Climate Data Store (CDS) API.

    Args:
        api_url: CDS API URL (default: https://cds.climate.copernicus.eu/api/v2)
        api_key: CDS API key in format "UID:API_KEY"
        roi: Region of interest as [west, south, east, north]
        start_date: Start date in 'YYYY-MM-DD' format
        end_date: End date in 'YYYY-MM-DD' format
        variables: List of variable names to fetch (ERA5 variable names)
        output_file: Output file path for NetCDF

    Returns:
        Path to downloaded ERA5 file
    """
    if not api_key:
        raise ValueError(
            "CDS_API_KEY not configured. "
            "Get API key from https://cds.climate.copernicus.eu/user/login and "
            "set in environment as CDS_API_KEY=UID:API_KEY"
        )

    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Default ERA5 variables
    if variables is None:
        variables = [
            "2m_temperature",
            "total_precipitation",
            "volumetric_soil_water_layer_1",
            "volumetric_soil_water_layer_2",
        ]

    # Map common names to CDS variable names
    variable_mapping = {
        "temperature_2m": "2m_temperature",
        "total_precipitation_sum": "total_precipitation",
        "volumetric_soil_water_layer_1": "volumetric_soil_water_layer_1",
        "volumetric_soil_water_layer_2": "volumetric_soil_water_layer_2",
    }

    # Translate variable names if needed
    era5_variables = []
    for var in variables:
        era5_variables.append(variable_mapping.get(var, var))

    try:
        # Initialize CDS client
        client = cdsapi.Client(
            url=api_url,
            key=api_key,
            quiet=False,
            debug=False,
        )

        # Parse dates
        start_dt = datetime.strptime(start_date, "%Y-%m-%d")
        end_dt = datetime.strptime(end_date, "%Y-%m-%d")

        # CDS API expects bounding box as [north, west, south, east]
        north, west, south, east = roi[3], roi[0], roi[1], roi[2]

        logger.info(
            "Requesting ERA5 data from CDS API for ROI: N={}, S={}, E={}, W={}, dates {} to {}",
            north,
            south,
            east,
            west,
            start_date,
            end_date,
        )

        # Request ERA5 reanalysis data
        client.retrieve(
            "reanalysis-era5-single-levels-monthly-means",
            {
                "product_type": "monthly_averaged_reanalysis",
                "variable": era5_variables,
                "year": [str(y) for y in range(start_dt.year, end_dt.year + 1)],
                "month": [f"{m:02d}" for m in range(1, 13)],
                "time": "00:00",
                "area": [north, west, south, east],
                "format": "netcdf",
            },
            str(output_path),
        )

        logger.info("Downloaded ERA5 data from CDS API to {}", output_path)
        return str(output_path)

    except Exception as e:
        logger.error(
            "Failed to download ERA5 data from CDS API to {} with variables {}: {}",
            output_path,
            variables,
            e,
        )
        raise
