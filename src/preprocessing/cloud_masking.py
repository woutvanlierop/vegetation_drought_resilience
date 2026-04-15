"""
Cloud masking and QA filtering for Sentinel-2 imagery.

Sentinel-2 includes QA bands (SCL, QA60) for cloud, shadow, and snow detection.
"""

from typing import Optional

import ee
import numpy as np


def apply_cloud_mask(
    image: ee.Image,
    qa_band_name: str = "QA60",
    band_names: Optional[list] = None,
) -> ee.Image:
    """
    Apply cloud mask to Sentinel-2 image using QA60 band.

    The QA60 band uses specific bit patterns to indicate:
    - Bit 10: Opaque clouds
    - Bit 11: Cirrus clouds

    Args:
        image: ee.Image (Sentinel-2 scene)
        qa_band_name: QA band name ('QA60' for S2L1C, 'SCL' for S2L2A)
        band_names: List of bands to retain (all if None)

    Returns:
        Masked ee.Image with cloud pixels set to null

    Example:
        >>> s2_masked = apply_cloud_mask(s2_scene)
    """
    # TODO: Implement bit masking
    # - Extract QA60 band
    # - Create mask for bits 10, 11
    # - Apply to bands
    # - Return masked image
    pass


def filter_by_cloud_cover(
    collection: ee.ImageCollection,
    max_percentage: float = 20,
) -> ee.ImageCollection:
    """
    Filter ImageCollection to exclude high-cloud-cover scenes.

    Args:
        collection: ee.ImageCollection of Sentinel-2 scenes
        max_percentage: Maximum allowed cloud cover (default 20%)

    Returns:
        Filtered ee.ImageCollection

    Example:
        >>> s2_clean = filter_by_cloud_cover(s2_collection, max_percentage=15)
    """
    # TODO: Implement cloud cover filtering
    # - Use CLOUD_COVER or CLOUDY_PIXEL_PERCENTAGE property
    # - Filter collection
    # - Return filtered collection
    pass


def apply_scl_mask(
    image: ee.Image,
    exclude_classes: Optional[list] = None,
) -> ee.Image:
    """
    Apply Scene Classification Layer (SCL) band masking for Sentinel-2 L2A.

    SCL classes:
    - 0: No Data
    - 1: Saturated/Defective
    - 2: Dark Area Pixels
    - 3: Cloud Shadows
    - 4: Vegetation
    - 5: Non-Vegetated
    - 6: Water
    - 7: Unclassified
    - 8: Cloud Medium Probability
    - 9: Cloud High Probability
    - 10: Thin Cirrus
    - 11: Snow/Ice

    Args:
        image: ee.Image with SCL band
        exclude_classes: SCL classes to mask out (default: [0,1,3,8,9,10,11])
            Excludes: No Data, Defective, Shadows, Medium Cloud, High Cloud, Cirrus, Snow

    Returns:
        Masked ee.Image
    """
    # TODO: Implement SCL masking
    # - Extract SCL band
    # - Mask specified classes
    # - Apply to image
    pass


def apply_ndvi_threshold(
    image: ee.Image,
    low_threshold: float = 0.3,
    nir_band: str = "B8",
    red_band: str = "B4",
) -> ee.Image:
    """
    Apply NDVI-based masking to exclude very low-NDVI pixels (water, bare soil, cloud).

    Args:
        image: ee.Image with NIR and Red bands
        low_threshold: Minimum NDVI value (default 0.3)
        nir_band: NIR band name
        red_band: Red band name

    Returns:
        Masked ee.Image with low-NDVI pixels set to null
    """
    # TODO: Implement NDVI threshold masking
    # - Calculate NDVI: (NIR - Red) / (NIR + Red)
    # - Create mask where NDVI >= threshold
    # - Apply to image
    pass
