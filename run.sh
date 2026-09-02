#!/usr/bin/env bash

# Exit immediately if a command exits with a non-zero status
set -e

# Set timezone explicitly for Oslo
export TZ="Europe/Oslo"

# Automatically locate the folder where run.sh is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Define paths relative to the script directory
PATH_TO_PYTHON="$SCRIPT_DIR/.venv/bin/python"
PATH_TO_SCRIPT="$SCRIPT_DIR/main.py"
LOG_FILE="$SCRIPT_DIR/cron.log"

# Change to the script directory so relative file imports inside main.py work
cd "$SCRIPT_DIR"

# Execute script and append output to log
echo "[$(date '+%Y-%m-%d %H:%M:%S %Z')] Executing main.py..." >> "$LOG_FILE"
"$PATH_TO_PYTHON" "$PATH_TO_SCRIPT" >> "$LOG_FILE" 2>&1
