#!/bin/bash

# Windsurf Privacy Toolkit Launcher
# This script finds and launches the toolkit from anywhere

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Navigate to script directory
cd "$SCRIPT_DIR"

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    osascript -e 'display dialog "Python 3 is required but not found. Please install Python 3." buttons {"OK"} default button "OK" with icon stop'
    exit 1
fi

# Check if GUI file exists
if [ ! -f "windsurf_privacy_gui.py" ]; then
    osascript -e 'display dialog "windsurf_privacy_gui.py not found in this directory!" buttons {"OK"} default button "OK" with icon stop'
    exit 1
fi

# Launch the GUI
python3 windsurf_privacy_gui.py

# If GUI exits with error, show message
if [ $? -ne 0 ]; then
    osascript -e 'display dialog "Error launching Windsurf Privacy Toolkit. Check terminal for details." buttons {"OK"} default button "OK" with icon caution'
fi
