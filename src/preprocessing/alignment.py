"""
Spatial and temporal alignment of satellite and weather data.

Handles:
- Clipping to region of interest
- Resampling to common resolution (100m target)
- Temporal alignment
- Coordinate system standardization
"""

from typing import Optional, Tuple

import ee
import xarray as xr


def clip_to_region(
    image: ee.Image,
    roi: list,
) -> ee.Image:
    """
    Clip image to region of interest.

    Args:
        image: ee.Image to clip
        roi: Bounding box [west, south, east, north]

    Returns:
        Clipped ee.Image

    Example:
        >>> bbox = [2.754, 50.674, 5.918, 51.507]  # Flanders
        >>> clipped = clip_to_region(image, bbox)
    """
    # TODO: Implement GEE clipping
    # - Create geometry from bbox
    # - Apply clip()
    # - Return clipped image
    pass


def resample_to_common_grid(
    sentinel_image: ee.Image,
    era5_dataset: xr.Dataset,
    target_resolution: int = 100,
) -> Tuple[ee.Image, xr.Dataset]:
    """
    Resample Sentinel-2 and ERA5 to common resolution and grid.

    Strategy:
    - Sentinel-2 (10m): Reproject to target resolution using nearest neighbor for integer data
    - ERA5 (25km): Bilinear interpolation to target grid
    - Align to common CRS (EPSG:4326 or EPSG:3857)

    Args:
        sentinel_image: Sentinel-2 ee.Image (10m resolution)
        era5_dataset: ERA5 xarray.Dataset (25km resolution)
        target_resolution: Target resolution in meters (default 100m)

    Returns:
        Tuple of (resampled_sentinel, resampled_era5)
    """
    # TODO: Implement resampling
    # - Define target CRS and grid (e.g., EPSG:3857)
    # - Resample Sentinel-2 via GEE projection
    # - Resample ERA5 via xarray interpolation
    # - Ensure spatial alignment
    pass


def align_temporal(
    sentinel_collection: ee.ImageCollection,
    era5_dataset: xr.Dataset,
    date_range: Optional[Tuple[str, str]] = None,
) -> Tuple[ee.ImageCollection, xr.Dataset]:
    """
    Align temporal dimensions of Sentinel-2 and ERA5 data.

    Strategy:
    - Sentinel-2: Keep all available scenes
    - ERA5: Resample to Sentinel-2 dates (daily data, already aligned)
    - If dates don't align perfectly, use nearest-date interpolation

    Args:
        sentinel_collection: ee.ImageCollection of Sentinel-2
        era5_dataset: xarray.Dataset of ERA5
        date_range: Optional tuple (start_date, end_date) to filter

    Returns:
        Tuple of (aligned_sentinel_collection, aligned_era5_dataset)
    """
    # TODO: Implement temporal alignment
    # - Extract dates from each dataset
    # - Filter to common date range
    # - Interpolate/aggregate as needed
    pass


def reproject_image(
    image: ee.Image,
    crs: str = "EPSG:4326",
    scale: int = 100,
) -> ee.Image:
    """
    Reproject image to specified CRS and resolution.

    Args:
        image: ee.Image to reproject
        crs: Target coordinate reference system (default EPSG:4326 - WGS84)
        scale: Output resolution in meters

    Returns:
        Reprojected ee.Image
    """
    # TODO: Implement GEE reprojection
    # - Use reproject() method
    # - Set CRS and scale
    # - Return reprojected image
    pass


def create_mosaic(
    collection: ee.ImageCollection,
    composite_method: str = "median",
) -> ee.Image:
    """
    Create composite image from collection using specified method.

    Methods:
    - 'median': Pixel-wise median (robust to outliers)
    - 'mean': Pixel-wise mean
    - 'max': Maximum NDVI composite (for vegetation monitoring)

    Args:
        collection: ee.ImageCollection to composite
        composite_method: Compositing method

    Returns:
        Composite ee.Image
    """
    # TODO: Implement compositing
    # - Apply appropriate reducer (ee.Reducer.median(), etc.)
    # - Return composite image
    pass
