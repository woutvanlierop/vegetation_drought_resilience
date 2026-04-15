"""
Pytest configuration and fixtures for drought monitoring tests.
"""

import logging
from pathlib import Path
from typing import Generator

import pytest
from dotenv import load_dotenv

# Load environment variables for testing
load_dotenv()


# ============================================================================
# Fixtures
# ============================================================================


@pytest.fixture
def test_data_dir() -> Path:
    """Return path to test data directory."""
    return Path(__file__).parent / "data"


@pytest.fixture
def flanders_bbox() -> list:
    """Return Flanders bounding box [west, south, east, north]."""
    return [2.754, 50.674, 5.918, 51.507]


@pytest.fixture
def caplog_with_level(caplog):
    """Fixture to capture logs at all levels."""
    caplog.set_level(logging.DEBUG)
    return caplog


# ============================================================================
# Markers
# ============================================================================


def pytest_configure(config):
    """Register custom pytest markers."""
    config.addinivalue_line(
        "markers",
        "integration: marks tests as integration tests (require external services like GEE, DB)",
    )
    config.addinivalue_line("markers", "slow: marks tests as slow running")
    config.addinivalue_line("markers", "gee: marks tests that interact with Google Earth Engine")
    config.addinivalue_line("markers", "database: marks tests that interact with PostGIS database")
