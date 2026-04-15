"""
Command-line interface for vegetation drought resilience operations.

This module provides CLI commands for data fetching, processing, and analysis.
"""

import argparse
import sys
from pathlib import Path
from typing import Optional

from loguru import logger

from src.config import get_settings
from src.data.fetchers import (
    authenticate_openeo,
    download_to_netcdf,
    fetch_era5_daily,
    fetch_sentinel2,
)
from src.utils.logging_config import setup_logging


def setup_cli_logging(verbose: bool = False) -> None:
    """Configure logging for CLI operations."""
    if verbose:
        logger.remove()  # Remove default handler
        logger.add(sys.stderr, level="DEBUG")
    else:
        logger.remove()  # Remove default handler
        logger.add(sys.stderr, level="INFO")


def fetch_data_command(
    start_date: str,
    end_date: str,
    output_dir: Optional[Path] = None,
    roi: Optional[list] = None,
    max_cloud_cover: int = 20,
    dry_run: bool = False,
) -> None:
    """
    Fetch Sentinel-2 and ERA5 data for the specified date range.

    Args:
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format
        output_dir: Output directory for downloaded files
        roi: Region of interest as [west, south, east, north]
        max_cloud_cover: Maximum cloud cover percentage for Sentinel-2
        dry_run: If True, only show what would be downloaded
    """
    settings = get_settings()

    # Use settings defaults if not provided
    if output_dir is None:
        output_dir = settings.RAW_DATA_DIR
    if roi is None:
        roi = settings.ROI_BBOX_LIST

    logger.info("Starting data fetch for %s to %s", start_date, end_date)
    logger.info("ROI: %s", roi)
    logger.info("Output directory: %s", output_dir)
    logger.info("Max cloud cover: %d%%", max_cloud_cover)

    if dry_run:
        logger.info("DRY RUN: Would fetch Sentinel-2 and ERA5 data")
        return

    try:
        # Fetch Sentinel-2 data
        logger.info("Fetching Sentinel-2 data...")
        s2_cube = fetch_sentinel2(
            backend_url=settings.OPENEO_BACKEND_URL,
            client_id=settings.OPENEO_CLIENT_ID,
            client_secret=settings.OPENEO_CLIENT_SECRET,
            provider_id=settings.OPENEO_AUTH_PROVIDER_ID,
            roi=roi,
            start_date=start_date,
            end_date=end_date,
            max_cloud_cover=max_cloud_cover,
            bands=settings.SENTINEL2_BANDS,
            collection_id=settings.OPENEO_SENTINEL2_COLLECTION_ID,
        )

        # Download Sentinel-2 to NetCDF
        s2_output = output_dir / f"sentinel2_{start_date}_{end_date}.nc"
        download_to_netcdf(s2_cube, str(s2_output), format="netcdf")
        logger.success("Downloaded Sentinel-2 data to %s", s2_output)

        # Fetch ERA5 data
        logger.info("Fetching ERA5 data...")
        era5_cube = fetch_era5_daily(
            backend_url=settings.OPENEO_BACKEND_URL,
            client_id=settings.OPENEO_CLIENT_ID,
            client_secret=settings.OPENEO_CLIENT_SECRET,
            provider_id=settings.OPENEO_AUTH_PROVIDER_ID,
            roi=roi,
            start_date=start_date,
            end_date=end_date,
            variables=settings.ERA5_VARIABLES,
            collection_id=settings.OPENEO_ERA5_COLLECTION_ID,
        )

        # Download ERA5 to NetCDF
        era5_output = output_dir / f"era5_{start_date}_{end_date}.nc"
        download_to_netcdf(era5_cube, str(era5_output), format="netcdf")
        logger.success("Downloaded ERA5 data to %s", era5_output)

        logger.success("Data fetch completed successfully!")

    except Exception as e:
        logger.error("Data fetch failed: %s", e)
        sys.exit(1)


def main() -> None:
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Vegetation Drought Resilience CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Fetch data for July 2023 (default ROI: Flanders)
  python -m src.cli fetch-data 2023-07-01 2023-07-31

  # Fetch data with custom ROI and output directory
  python -m src.cli fetch-data 2023-07-01 2023-07-31 \\
    --roi 2.5 50.5 6.0 51.5 \\
    --output-dir ./custom_data \\
    --max-cloud-cover 10

  # Dry run to see what would be downloaded
  python -m src.cli fetch-data 2023-07-01 2023-07-31 --dry-run
        """,
    )

    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose logging",
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Fetch data command
    fetch_parser = subparsers.add_parser(
        "fetch-data",
        help="Fetch Sentinel-2 and ERA5 data from OpenEO",
    )
    fetch_parser.add_argument(
        "start_date",
        help="Start date in YYYY-MM-DD format",
    )
    fetch_parser.add_argument(
        "end_date",
        help="End date in YYYY-MM-DD format",
    )
    fetch_parser.add_argument(
        "--output-dir",
        type=Path,
        help="Output directory for downloaded files (default: data/raw)",
    )
    fetch_parser.add_argument(
        "--roi",
        nargs=4,
        type=float,
        metavar=("WEST", "SOUTH", "EAST", "NORTH"),
        help="Region of interest bounds (default: Flanders)",
    )
    fetch_parser.add_argument(
        "--max-cloud-cover",
        type=int,
        default=20,
        help="Maximum cloud cover percentage for Sentinel-2 (default: 20)",
    )
    fetch_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be downloaded without actually fetching",
    )

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    # Setup logging
    setup_cli_logging(verbose=args.verbose)

    # Setup logging config
    setup_logging()

    # Execute command
    if args.command == "fetch-data":
        fetch_data_command(
            start_date=args.start_date,
            end_date=args.end_date,
            output_dir=args.output_dir,
            roi=args.roi,
            max_cloud_cover=args.max_cloud_cover,
            dry_run=args.dry_run,
        )
    else:
        logger.error("Unknown command: %s", args.command)
        sys.exit(1)


if __name__ == "__main__":
    main()