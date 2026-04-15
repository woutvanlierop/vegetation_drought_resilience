"""
OpenEO data fetchers for Sentinel-2 and ERA5 weather data via Copernicus.

This module handles all data download operations from OpenEO backends.
Supports multiple backends:
- EODC (https://openeo.creo.vito.be) — European Open Data Cube
- CDSE (https://openeo.dataspace.copernicus.eu) — Copernicus Data Space Ecosystem (free)
- Sentinel Hub
"""

from datetime import datetime
from pathlib import Path
from typing import Optional, Tuple

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
        logger.info("Authenticated with OpenEO backend: %s", backend_url)
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
            "Loaded Sentinel-2 collection %s for %s to %s",
            collection_id,
            start_date,
            end_date,
        )
        return cube
    except Exception as e:
        logger.error("Failed to load Sentinel-2 collection %s: %s", collection_id, e)
        raise


def fetch_era5_daily(
    backend_url: str,
    client_id: Optional[str],
    client_secret: Optional[str],
    provider_id: Optional[str],
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
            "Loaded ERA5 collection %s for %s to %s",
            collection_id,
            start_date,
            end_date,
        )
        return cube
    except Exception as e:
        logger.error("Failed to load ERA5 collection %s: %s", collection_id, e)
        raise


def download_to_netcdf(
    datacube: openeo.DataCube,
    output_file: str,
    format: str = "netcdf",
) -> str:
    """
    Download OpenEO DataCube to NetCDF file.

    Args:
        datacube: openeo.DataCube to download
        output_file: Output file path
        format: Output format ('netcdf', 'GeoTIFF', 'COG', etc.)

    Returns:
        Path to downloaded file
    """
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        datacube.download(outputfile=output_path, format=format)
        logger.info("Downloaded OpenEO result to %s", output_path)
        return str(output_path)
    except Exception as e:
        logger.error(
            "Failed to download OpenEO result to %s with format %s: %s",
            output_path,
            format,
            e,
        )
        raise


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
        logger.info("Downloaded OpenEO result to %s", output_path)
        return str(output_path)
    except Exception as e:
        logger.error("Failed to download OpenEO COG to %s: %s", output_path, e)
        raise
