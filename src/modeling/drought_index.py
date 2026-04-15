"""
Composite drought index modeling.

Implements Percentile-Based Multi-Component Drought Index (PMDI):
- Standardized Precipitation Index (SPI)
- Vegetation Stress Index (VSI)
- Soil Moisture Percentile
"""

from typing import Dict, Optional, Tuple

import numpy as np
import xarray as xr
from loguru import logger


class DroughtIndex:
    """
    Compute and classify drought using multi-component index.

    Components:
    1. SPI (Standardized Precipitation Index) — WMO standard
    2. VSI (Vegetation Stress Index) — remote sensing standard
    3. SM Percentile — soil moisture anomaly

    Fusion: Median of ranked components
    Classification: Adaptive percentile thresholds
    """

    def __init__(
        self,
        baseline_years: Tuple[int, int] = (2016, 2022),
        region: str = "flanders",
        spi_weight: float = 0.35,
        vsi_weight: float = 0.35,
        sm_weight: float = 0.30,
    ):
        """
        Initialize drought model with baseline period.

        Args:
            baseline_years: Tuple (start_year, end_year) for baseline period
            region: Region name for configuration
            spi_weight: Weight for SPI component (if not using percentile fusion)
            vsi_weight: Weight for VSI component
            sm_weight: Weight for SM component
        """
        self.baseline_years = baseline_years
        self.region = region
        self.spi_weight = spi_weight
        self.vsi_weight = vsi_weight
        self.sm_weight = sm_weight

        # Verify weights sum correctly if using weighted fusion
        total_weight = spi_weight + vsi_weight + sm_weight
        if not np.isclose(total_weight, 1.0):
            logger.warning(
                f"Component weights sum to {total_weight}, not 1.0. "
                "Consider normalization if using weighted fusion."
            )

    def compute_spi(
        self,
        precipitation: xr.DataArray,
        baseline_distribution: Optional[Dict] = None,
    ) -> xr.DataArray:
        """
        Compute Standardized Precipitation Index.

        Args:
            precipitation: Monthly precipitation data
            baseline_distribution: Dict with 'mean' and 'std' from baseline

        Returns:
            SPI values in [-3, +3] scale
        """
        # TODO: Implement SPI computation
        # - Load or use provided baseline
        # - Standardize current precipitation
        # - Return SPI
        pass

    def compute_vsi(
        self,
        ndvi_current: xr.DataArray,
        ndvi_baseline_climatology: xr.DataArray,
    ) -> xr.DataArray:
        """
        Compute Vegetation Stress Index.

        VSI = 1 - (NDVI_current / NDVI_p50_baseline)

        Args:
            ndvi_current: Current month NDVI
            ndvi_baseline_climatology: Baseline NDVI (p50 for that month from 2016-2022)

        Returns:
            VSI [0, 1] where 0 = healthy, >0.3 = stressed
        """
        # TODO: Implement VSI computation
        # - Align arrays
        # - Apply formula
        # - Handle division by zero
        # - Return VSI
        pass

    def compute_soil_moisture_percentile(
        self,
        soil_moisture_current: xr.DataArray,
        soil_moisture_cdf: xr.DataArray,
    ) -> xr.DataArray:
        """
        Compute soil moisture percentile rank.

        Args:
            soil_moisture_current: Current soil moisture
            soil_moisture_cdf: Empirical CDF from baseline period

        Returns:
            Percentile rank [0, 1] where 0 = very wet, 1 = very dry
        """
        # TODO: Implement percentile ranking
        pass

    def compute_composite_drought_index(
        self,
        spi: xr.DataArray,
        vsi: xr.DataArray,
        sm_percentile: xr.DataArray,
        method: str = "percentile_median",
    ) -> xr.DataArray:
        """
        Combine three components into composite drought index.

        Methods:
        - 'percentile_median': Median of percentile-ranked components (recommended)
        - 'weighted': Weighted average with configured weights

        Args:
            spi: Standardized Precipitation Index
            vsi: Vegetation Stress Index [0, 1]
            sm_percentile: Soil moisture percentile [0, 1]
            method: Fusion method

        Returns:
            Composite Drought Index CDI [0, 1]
                0 = no drought, 1 = extreme drought
        """
        # TODO: Implement fusion
        # - Normalize components to [0, 1]
        # - Apply selected fusion method
        # - Return CDI
        pass

    def classify_severity_adaptive(
        self,
        cdi_spatial_array: xr.DataArray,
    ) -> xr.DataArray:
        """
        Classify drought severity using percentile-based thresholds.

        Thresholds adapt to observed CDI distribution in region:
        - No drought: CDI < 20th percentile
        - Mild: 20–40th percentile
        - Moderate: 40–70th percentile
        - Severe: > 70th percentile

        Args:
            cdi_spatial_array: Spatial CDI map

        Returns:
            Classification map with categories
                {'no_drought', 'mild', 'moderate', 'severe'}
        """
        # TODO: Implement adaptive classification
        # - Compute CDI percentiles in region
        # - Assign categories based on percentile
        # - Return classification
        pass

    def compute_confidence(
        self,
        components: Dict[str, xr.DataArray],
    ) -> xr.DataArray:
        """
        Compute confidence score from component agreement.

        High confidence: All three components agree on drought signal
        Low confidence: Components disagree (flag for manual review)

        Args:
            components: Dict with 'spi', 'vsi', 'sm_pct' components

        Returns:
            Confidence score [0, 1]
        """
        # TODO: Implement confidence scoring
        # - Rank components
        # - Compute scatter/disagreement
        # - Return confidence [0, 1]
        pass
