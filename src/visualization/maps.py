"""
Geospatial map visualization using Folium.
"""

from pathlib import Path
from typing import Optional

import folium
import geopandas as gpd
import xarray as xr


def create_drought_map(
    drought_raster: xr.DataArray,
    roi_geom: Optional[gpd.GeoDataFrame] = None,
    color_palette: str = "RdYlGn_r",
    legend_title: str = "Drought Severity",
    vmin: float = 0.0,
    vmax: float = 1.0,
    zoom_start: int = 8,
    center_lat: float = 51.1,
    center_lng: float = 4.4,
) -> folium.Map:
    """
    Create interactive Folium map of drought severity.

    Args:
        drought_raster: xarray.DataArray with drought severity (0-1)
        roi_geom: Optional GeoDataFrame with region boundaries
        color_palette: Matplotlib color palette ('RdYlGn_r' recommended)
        legend_title: Title for map legend
        vmin, vmax: Value range for color mapping
        zoom_start: Initial zoom level
        center_lat, center_lng: Map center coordinates

    Returns:
        folium.Map object ready to display/save

    Example:
        >>> map_obj = create_drought_map(cdi_spatial, roi_gdf)
        >>> map_obj.save('drought_map.html')
    """
    # TODO: Implement Folium map creation
    # - Create base map
    # - Add drought raster as layer
    # - Add region overlays if provided
    # - Add legend and colorbar
    # - Return map object
    pass


def add_region_overlay(
    map_obj: folium.Map,
    gdf_regions: gpd.GeoDataFrame,
    name: str = "Regions",
    color: str = "black",
    weight: int = 2,
    opacity: float = 0.8,
) -> folium.Map:
    """
    Add region boundaries overlay to map.

    Args:
        map_obj: Existing Folium map
        gdf_regions: GeoDataFrame with region geometries
        name: Layer name
        color: Boundary color
        weight: Line weight
        opacity: Line opacity

    Returns:
        Updated folium.Map
    """
    # TODO: Implement GeoDataFrame overlay
    # - Convert to GeoJSON
    # - Add to map as layer
    # - Add popup with region names
    # - Return updated map
    pass


def save_map_html(
    map_obj: folium.Map,
    filename: str,
    directory: Optional[Path] = None,
) -> str:
    """
    Save Folium map to HTML file.

    Args:
        map_obj: Folium Map object
        filename: Output filename (with .html extension)
        directory: Output director (default current directory)

    Returns:
        Full path to saved file
    """
    # TODO: Implement HTML save
    # - Validate filename
    # - Create directory if needed
    # - Save map
    # - Return file path
    pass


def create_comparison_map(
    drought_before: xr.DataArray,
    drought_after: xr.DataArray,
    labels: tuple = ("Before", "After"),
) -> folium.Map:
    """
    Create side-by-side comparison map.

    Args:
        drought_before: Drought severity map (baseline or earlier date)
        drought_after: Drought severity map (comparison date)
        labels: Tuple of labels for before/after

    Returns:
        Folium map with layer control
    """
    # TODO: Implement comparison map
    # - Create base map
    # - Add two layers (before, after)
    # - Add layer control
    # - Return map
    pass
