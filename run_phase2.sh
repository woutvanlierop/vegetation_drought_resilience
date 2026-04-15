#!/bin/bash
# Shell script to run Phase 2 data fetching for vegetation drought resilience
# Usage: ./run_phase2.sh [start_date] [end_date] [options]

if [ $# -eq 0 ]; then
    echo "Usage: $0 START_DATE END_DATE [options]"
    echo
    echo "Example: $0 2023-07-01 2023-07-31"
    echo "Example: $0 2023-07-01 2023-07-31 --dry-run"
    echo "Example: $0 2023-07-01 2023-07-31 --roi 2.5 50.5 6.0 51.5"
    echo
    echo "Options:"
    echo "  --dry-run                    Show what would be downloaded"
    echo "  --roi WEST SOUTH EAST NORTH  Custom region of interest"
    echo "  --output-dir PATH           Custom output directory"
    echo "  --max-cloud-cover PERCENT   Maximum cloud cover (default: 20)"
    echo "  --verbose                   Enable verbose logging"
    exit 1
fi

# Activate virtual environment if it exists
if [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate
elif [ -f ".venv/Scripts/activate" ]; then
    source .venv/Scripts/activate
fi

# Run the CLI command
python -m src.cli fetch-data "$@"