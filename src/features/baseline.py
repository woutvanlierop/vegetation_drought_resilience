"""
Historical baseline computation for drought detection.

Computes:
- NDVI climatology (per month)
- Precipitation climatology
- Soil moisture climatology (including percentiles)
"""

from typing import Dict, List, Optional, Tuple

import xarray as xr


def compute_historical_baseline(
    era5_archive: xr.Dataset,
    baseline_years: Optional[List[int]] = None,
) -> xr.Dataset:
    """
    Compute historical baseline from ERA5 archive.

    For each month, computes:
    - Mean, std dev, min, max
    - Quantiles (25th, 50th, 75th percentiles)

    Args:
        era5_archive: Full archive of ERA5 data (multiple years)
        baseline_years: List of years to use for baseline (default 2016-2022)

    Returns:
        xarray.Dataset with baseline statistics
            Dimensions: (month, variable)
            Data: {mean, std, min, max, p25, p50, p75}
    """
    # TODO: Implement baseline computation
    # - Filter to baseline years
    # - Group by month
    # - Compute statistics
    # - Return as Dataset
    pass


def compute_ndvi_baseline(
    sentinel2_archive: xr.DataArray,
    baseline_years: Optional[List[int]] = None,
    months: Optional[List[int]] = None,
) -> xr.DataArray:
    """
    Compute NDVI baseline (climatology) from Sentinel-2 archive.

    For each month, computes percentiles of NDVI from baseline years.

    Args:
        sentinel2_archive: NDVI time series from Sentinel-2
        baseline_years: Years to use for baseline (default 2016-2022)
        months: Months to compute baseline for (default: all months)

    Returns:
        xarray.DataArray with NDVI baseline (p50 values per month)
    """
    # TODO: Implement NDVI baseline
    # - Filter to baseline years
    # - Group by month
    # - Compute percentiles
    # - Return baseline
    pass


def load_baseline_from_db(
    index_name: str,
    month: int,
) -> Dict:
    """
    Load pre-computed baseline from PostGIS database.

    Args:
        index_name: Type of baseline {'ndvi', 'spi', 'sm'}
        month: Month (1-12)

    Returns:
        Dictionary with baseline statistics
    """
    # TODO: Implement database query
    # - Connect to database
    # - Query baseline_stats table
    # - Return statistics
    pass


def save_baseline_to_db(
    baseline_dict: Dict,
    index_name: str,
) -> None:
    """
    Save computed baseline to PostGIS database.

    Args:
        baseline_dict: Dictionary with baseline statistics
        index_name: Type of baseline to save
    """
    # TODO: Implement database insert
    # - Connect to database
    # - Insert into baseline_stats table
    # - Handle updates (upsert)
    pass


def compute_soil_moisture_cdf(
    soil_moisture_archive: xr.DataArray,
    baseline_years: Optional[List[int]] = None,
) -> xr.DataArray:
    """
    Compute cumulative distribution function (CDF) of soil moisture.

    Used to rank current soil moisture percentile.

    Args:
        soil_moisture_archive: Historical SM time series
        baseline_years: Years to use (default 2016-2022)

    Returns:
        xarray.DataArray with empirical CDF
            Can be used with rankdata or searchsorted
    """
    # TODO: Implement CDF computation
    # - Filter to baseline years
    # - Compute empirical CDF per grid cell
    # - Return as Dataset
    pass


def initialize_baseline(
    gee_project_id: str,
    roi_bbox: List[float],
    output_db_connection: str,
) -> None:
    """
    Initialize baseline statistics for first-time setup.

    Fetches 2016-2022 data from GEE, computes baselines, saves to PostGIS.

    Args:
        gee_project_id: Google Earth Engine project ID
        roi_bbox: Region of interest [west, south, east, north]
        output_db_connection: PostgreSQL connection string
    """
    # TODO: Implement full baseline initialization
    # - Fetch 2016-2022 data
    # - Compute NDVI, SPI, SM baselines
    # - Save to database
    # - Provide progress feedback
    pass
