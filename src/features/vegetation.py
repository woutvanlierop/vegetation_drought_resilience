"""
Vegetation index computation from Sentinel-2 imagery.

Standard indices:
- NDVI: Normalized Difference Vegetation Index
- NDWI: Normalized Difference Water Index
- EVI: Enhanced Vegetation Index
"""

from typing import Optional

import ee
import numpy as np
import xarray as xr


def compute_ndvi(
    image: ee.Image,
    nir_band: str = "B8",
    red_band: str = "B4",
    scale_factor: float = 1e4,
) -> ee.Image:
    """
    Compute Normalized Difference Vegetation Index (NDVI).

    NDVI = (NIR - Red) / (NIR + Red)

    Standard interpretation:
    - NDVI < 0: Water, snow
    - NDVI 0-0.2: Bare soil, urban
    - NDVI 0.2-0.5: Sparse/degraded vegetation
    - NDVI 0.5+: Dense vegetation

    Args:
        image: ee.Image with NIR and Red bands
        nir_band: NIR band name (Sentinel-2: 'B8')
        red_band: Red band name (Sentinel-2: 'B4')
        scale_factor: Factor to scale band values (Sentinel-2 uses 10000)

    Returns:
        ee.Image with NDVI band

    Example:
        >>> ndvi = compute_ndvi(s2_image)
    """
    # TODO: Implement NDVI calculation
    # - Extract bands
    # - Apply formula: (NIR - Red) / (NIR + Red)
    # - Handle scale factor
    # - Return as single-band image
    pass


def compute_ndwi(
    image: ee.Image,
    nir_band: str = "B8",
    swir_band: str = "B11",
) -> ee.Image:
    """
    Compute Normalized Difference Water Index (NDWI).

    NDWI = (NIR - SWIR) / (NIR + SWIR)

    Measures water content in vegetation and soil. Useful for detecting:
    - Vegetation water stress
    - Irrigation patterns
    - Wetlands vs. dry areas

    Args:
        image: ee.Image with NIR and SWIR bands
        nir_band: NIR band name
        swir_band: SWIR band name (Sentinel-2: 'B11')

    Returns:
        ee.Image with NDWI band
    """
    # TODO: Implement NDWI calculation
    pass


def compute_evi(
    image: ee.Image,
    nir_band: str = "B8",
    red_band: str = "B4",
    blue_band: str = "B2",
    l: float = 1.0,
    c1: float = 6.0,
    c2: float = 7.5,
) -> ee.Image:
    """
    Compute Enhanced Vegetation Index (EVI).

    EVI = 2.5 * (NIR - Red) / (NIR + C1*Red - C2*Blue + L)

    More sensitive to canopy variations than NDVI, especially in dense vegetation.

    Args:
        image: ee.Image with NIR, Red, Blue bands
        nir_band: NIR band name
        red_band: Red band name
        blue_band: Blue band name (Sentinel-2: 'B2')
        l, c1, c2: Calibration constants (default standard values)

    Returns:
        ee.Image with EVI band
    """
    # TODO: Implement EVI calculation
    pass


def extract_ndvi_timeseries(
    collection: ee.ImageCollection,
    geometry: ee.Geometry,
) -> list:
    """
    Extract NDVI time series from collection at specific geometry.

    Args:
        collection: ee.ImageCollection with NDVI band
        geometry: ee.Geometry (point or small polygon)

    Returns:
        List of (date, NDVI value) tuples in chronological order
    """
    # TODO: Implement time series extraction
    # - Map over collection
    # - Sample at geometry
    # - Extract dates and values
    # - Return as list of tuples
    pass


def compute_ndvi_anomaly(
    ndvi: xr.DataArray,
    ndvi_baseline: xr.DataArray,
) -> xr.DataArray:
    """
    Compute NDVI anomaly relative to baseline.

    Anomaly = Current NDVI - Mean Baseline NDVI

    Args:
        ndvi: Current NDVI (xarray DataArray)
        ndvi_baseline: Baseline NDVI climatology

    Returns:
        NDVI anomaly (xarray DataArray)
    """
    # TODO: Implement anomaly computation
    # - Convert to common coordinates
    # - Subtract baseline
    # - Return difference
    pass
