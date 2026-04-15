"""
Weather anomaly computation from ERA5 data.

Computes:
- Standardized Precipitation Index (SPI)
- Temperature anomalies
- Soil moisture anomalies
"""

from typing import Optional, Tuple

import numpy as np
import xarray as xr
from scipy import stats


def compute_spi(
    precipitation: xr.DataArray,
    baseline_mean: xr.DataArray,
    baseline_std: xr.DataArray,
) -> xr.DataArray:
    """
    Compute Standardized Precipitation Index (SPI).

    SPI = (Precipitation - Mean) / Std Dev

    WMO standard for drought classification:
    - SPI ≥ 2: Extremely wet
    - SPI ≥ 1: Very wet
    - SPI < -1: Dry
    - SPI < -2: Severe drought
    - SPI < -3: Extreme drought

    Args:
        precipitation: Monthly precipitation (xarray DataArray)
        baseline_mean: Mean precipitation from baseline period
        baseline_std: Std dev precipitation from baseline period

    Returns:
        SPI values in [-3, +3] scale (xarray DataArray)

    Example:
        >>> spi = compute_spi(precip_july2023, precip_mean_sept, precip_std_july)
    """
    # TODO: Implement SPI calculation
    # - Standardize: (P - mean) / std
    # - Clip to [-3, +3] range
    # - Handle NaN/zero values
    pass


def compute_precipitation_deficit(
    precipitation: xr.DataArray,
    baseline_precipitation: xr.DataArray,
) -> xr.DataArray:
    """
    Compute precipitation deficit relative to baseline.

    Deficit = Mean Baseline - Current Precipitation

    Positive values indicate deficit (dry conditions).

    Args:
        precipitation: Current precipitation (mm/month)
        baseline_precipitation: Mean baseline precipitation

    Returns:
        Precipitation deficit (xarray DataArray)
    """
    # TODO: Implement deficit calculation
    # - Subtract current from baseline
    # - Return difference
    pass


def compute_temperature_anomaly(
    temperature: xr.DataArray,
    baseline_temperature: xr.DataArray,
) -> xr.DataArray:
    """
    Compute temperature anomaly relative to baseline.

    Anomaly = Current Temperature - Mean Baseline Temperature

    Positive values indicate warming.

    Args:
        temperature: Current temperature (°C)
        baseline_temperature: Mean baseline temperature

    Returns:
        Temperature anomaly in °C (xarray DataArray)
    """
    # TODO: Implement anomaly calculation
    # - Subtract baseline from current
    # - Return difference
    pass


def compute_soil_moisture_anomaly(
    soil_moisture: xr.DataArray,
    baseline_soil_moisture: xr.DataArray,
) -> xr.DataArray:
    """
    Compute soil moisture anomaly relative to baseline.

    Anomaly = Current SM - Mean Baseline SM

    Negative values indicate drier-than-normal soil.

    Args:
        soil_moisture: Current volumetric soil moisture (m³/m³)
        baseline_soil_moisture: Mean baseline soil moisture

    Returns:
        Soil moisture anomaly (xarray DataArray)
    """
    # TODO: Implement anomaly calculation
    pass


def compute_soil_moisture_percentile(
    soil_moisture: xr.DataArray,
    historical_distribution: xr.DataArray,
) -> xr.DataArray:
    """
    Rank soil moisture within historical distribution.

    Returns percentile rank: 0 = very wet, 1 = very dry (relative to 2016-2022 history).

    Args:
        soil_moisture: Current soil moisture (m³/m³)
        historical_distribution: Historical SM values (from 2016-2022)

    Returns:
        Percentile rank [0, 1] (xarray DataArray)
    """
    # TODO: Implement percentile ranking
    # - Compute empirical CDF or quantiles
    # - Rank current SM within distribution
    # - Return percentile [0, 1]
    pass
