"""
Main Streamlit dashboard application for drought monitoring.
"""

import streamlit as st

from src.config import get_settings
from src.utils.logging_config import setup_logging


def main() -> None:
    """
    Main Streamlit application entry point.

    Features:
    - Interactive drought map for Flanders
    - Filters: Land cover type, severity level, date range (MVP: static July 2023)
    - Summary statistics and regional breakdown
    - Time series analysis for selected regions
    """
    # TODO: Implement Streamlit dashboard
    # - Set up page config
    # - Add title and description
    # - Add sidebar filters
    # - Load and display drought map
    # - Add statistics and analysis sections
    pass


if __name__ == "__main__":
    # Setup logging
    setup_logging()

    # Get settings
    settings = get_settings()

    # Configure Streamlit page
    st.set_page_config(
        page_title="Drought Impact Monitoring",
        page_icon="🌍",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # Run main app
    main()
