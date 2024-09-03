#!/bin/bash

# Get the current directory
CURRENT_DIR="$(pwd)"

# Set environment variable to current directory
export APP_CONFIG_FILE="$CURRENT_DIR/config/development.py"

# Run Python script
python3 run.py

# Check if Python script execution was successful
if [ $? -ne 0 ]; then
    echo "Error: Python script execution failed."
    exit 1
fi 

echo "Build successful."


