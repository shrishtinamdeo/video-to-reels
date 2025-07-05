#!/bin/bash

echo "🎬 AI Video Reel Generator"
echo "========================="
echo ""
echo "Starting the application..."
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Run the application
python3 run.py 