@echo off
REM Batch script to run Phase 2 data fetching for vegetation drought resilience
REM Usage: run_phase2.bat [start_date] [end_date] [options]

if "%~1"=="" (
    echo Usage: run_phase2.bat START_DATE END_DATE [options]
    echo.
    echo Example: run_phase2.bat 2023-07-01 2023-07-31
    echo Example: run_phase2.bat 2023-07-01 2023-07-31 --dry-run
    echo Example: run_phase2.bat 2023-07-01 2023-07-31 --roi 2.5 50.5 6.0 51.5
    echo.
    echo Options:
    echo   --dry-run                    Show what would be downloaded
    echo   --roi WEST SOUTH EAST NORTH  Custom region of interest
    echo   --output-dir PATH           Custom output directory
    echo   --max-cloud-cover PERCENT   Maximum cloud cover (default: 20)
    echo   --verbose                   Enable verbose logging
    exit /b 1
)

REM Activate virtual environment if it exists
if exist ".venv\Scripts\activate.bat" (
    call .venv\Scripts\activate.bat
)

REM Run the CLI command
python -m src.cli fetch-data %*