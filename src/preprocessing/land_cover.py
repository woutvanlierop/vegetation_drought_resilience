"""
Land cover filtering and classification for natural area identification.

Uses ESA WorldCover 10m global map or CORINE Land Cover.
"""

from typing import List, Optional

import ee


def load_landcover_dataset(
    dataset_name: str = "ESA_WORLDCOVER",
    year: int = 2021,
) -> ee.Image:
    """
    Load land cover classification dataset.

    Supported datasets:
    - ESA_WORLDCOVER: 10m resolution, ESA/Copernicus
    - CORINE: 100m resolution, European coverage

    Args:
        dataset_name: Land cover dataset name
        year: Year of dataset

    Returns:
        ee.Image with land cover classification

    Example:
        >>> lc = load_landcover_dataset('ESA_WORLDCOVER', 2021)
    """
    # TODO: Implement land cover dataset loading
    # - Support multiple datasets
    # - Handle versioning
    # - Return Image with classification bands
    pass


def filter_by_landcover(
    collection: ee.ImageCollection,
    lc_image: Optional[ee.Image] = None,
    classes: Optional[List[str]] = None,
) -> ee.ImageCollection:
    """
    Filter image collection to only pixels matching specified land cover classes.

    Args:
        collection: ee.ImageCollection to filter
        lc_image: ee.Image with land cover classification (auto-loads if None)
        classes: List of class names to keep
            Options: ['forest', 'grassland', 'wetland', 'agricultural', 'urban', 'water']

    Returns:
        Filtered ee.ImageCollection with only specified land cover pixels

    Example:
        >>> s2_filtered = filter_by_landcover(s2_collection, classes=['forest', 'grassland'])
    """
    # TODO: Implement land cover filtering
    # - Load LC dataset if not provided
    # - Create mask for specified classes
    # - Apply to collection via map()
    # - Return filtered collection
    pass


def mask_non_natural(
    image: ee.Image,
    lc_image: Optional[ee.Image] = None,
    natural_classes: Optional[List[str]] = None,
) -> ee.Image:
    """
    Mask all non-natural pixels (urban, agricultural, water, bare soil).

    Useful for focusing on primary ecosystems: forests, grasslands, wetlands.

    Args:
        image: ee.Image to mask
        lc_image: Land cover image (auto-loads if None)
        natural_classes: Classes to keep as "natural"
            Default: ['forest', 'grassland', 'wetland', 'shrub', 'moss/lichen']

    Returns:
        Masked ee.Image with non-natural pixels as null
    """
    # TODO: Implement natural area masking
    # - Define natural LC classes
    # - Load LC dataset
    # - Create and apply mask
    pass


def get_landcover_class_ids(dataset_name: str = "ESA_WORLDCOVER") -> dict:
    """
    Get mapping of land cover class names to numeric IDs.

    ESA WorldCover classes:
    - 10: Tree Cover
    - 20: Shrubland
    - 30: Herbaceous Vegetation
    - 40: Cropland
    - 50: Built-up
    - 60: Bare/Sparse Vegetation
    - 70: Snow and Ice
    - 80: Permanent Water Bodies
    - 90: Herbaceous Wetland
    - 95: Mangroves
    - 100: Moss and Lichen

    Args:
        dataset_name: Land cover dataset

    Returns:
        Dictionary mapping class names to IDs
    """
    # TODO: Implement class ID mapping
    # - Define for each dataset
    # - Support name -> ID conversions
    pass
