"""
Logging configuration for drought monitoring system.
"""

import sys
from pathlib import Path

from loguru import logger

from src.config import get_settings


def setup_logging() -> None:
    """
    Configure logging with loguru.
    
    Sets up:
    - Console output (INFO level)
    - File output (DEBUG level)
    - Rotation and retention policies
    """
    settings = get_settings()

    # Remove default handler
    logger.remove()

    # Console handler (INFO level for cleaner output)
    logger.add(
        sys.stdout,
        format=(
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
            "<level>{message}</level>"
        ),
        level=settings.LOG_LEVEL,
        colorize=True,
    )

    # File handler (DEBUG level for detailed logging)
    logger.add(
        str(settings.LOG_FILE),
        format=(
            "{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | "
            "{name}:{function}:{line} - {message}"
        ),
        level="DEBUG",
        rotation="500 MB",  # Rotate when file reaches 500 MB
        retention="7 days",  # Keep logs for 7 days
    )

    logger.debug(f"Logging configured. Log file: {settings.LOG_FILE}")
