"""
Input validation utilities for drought monitoring system.
"""

from datetime import datetime
from typing import Tuple

import numpy as np
from loguru import logger


def validate_date_range(start_date: str, end_date: str, date_format: str = "%Y-%m-%d") -> Tuple[datetime, datetime]:
    """
    Validate and parse date range.
    
    Args:
        start_date: Start date string
        end_date: End date string
        date_format: Expected date format
        
    Returns:
        Tuple of (start_datetime, end_datetime)
        
    Raises:
        ValueError: If dates are invalid or start > end
    """
    try:
        start = datetime.strptime(start_date, date_format)
        end = datetime.strptime(end_date, date_format)
    except ValueError as e:
        logger.error(f"Invalid date format: {e}")
        raise ValueError(f"Invalid date format: {e}") from e

    if start > end:
        logger.error(f"Start date ({start}) must be before end date ({end})")
        raise ValueError("Start date must be before end date")

    return start, end


def validate_bbox(bbox: list, name: str = "bbox") -> bool:
    """
    Validate bounding box format [west, south, east, north].
    
    Args:
        bbox: Bounding box as [west, south, east, north]
        name: Name for error messages
        
    Returns:
        True if valid
        
    Raises:
        ValueError: If bbox is invalid
    """
    if not isinstance(bbox, (list, tuple)) or len(bbox) != 4:
        raise ValueError(f"{name} must be list/tuple of 4 values [west, south, east, north]")

    west, south, east, north = bbox

    if not (-180 <= west <= 180):
        raise ValueError(f"West longitude ({west}) out of range [-180, 180]")
    if not (-180 <= east <= 180):
        raise ValueError(f"East longitude ({east}) out of range [-180, 180]")
    if not (-90 <= south <= 90):
        raise ValueError(f"South latitude ({south}) out of range [-90, 90]")
    if not (-90 <= north <= 90):
        raise ValueError(f"North latitude ({north}) out of range [-90, 90]")

    if west >= east:
        raise ValueError(f"West ({west}) must be less than east ({east})")
    if south >= north:
        raise ValueError(f"South ({south}) must be less than north ({north})")

    return True


def validate_raster_data(data: np.ndarray, name: str = "raster") -> bool:
    """
    Validate raster data array.
    
    Args:
        data: NumPy array
        name: Name for error messages
        
    Returns:
        True if valid
        
    Raises:
        ValueError: If data is invalid
    """
    if not isinstance(data, np.ndarray):
        raise ValueError(f"{name} must be NumPy array, got {type(data)}")

    if data.ndim < 2:
        raise ValueError(f"{name} must be at least 2D, got {data.ndim}D")

    if np.isnan(data).all():
        raise ValueError(f"{name} is entirely NaN")

    return True
