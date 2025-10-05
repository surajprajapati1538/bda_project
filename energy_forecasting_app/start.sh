#!/bin/bash

# Energy Forecasting Application Launcher
# This script helps you quickly start either the Streamlit app or Flask API

echo "Energy Forecasting Application Launcher"
echo "=========================================="
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate  # For macOS/Linux
# For Windows use: venv\Scripts\activate

# Install requirements if needed
if [ ! -f "venv/pyvenv.cfg" ] || [ requirements.txt -nt venv/pyvenv.cfg ]; then
    echo "Installing requirements..."
    pip install -r requirements.txt
fi

echo ""
echo "Choose an option:"
echo "1. Start Streamlit Web App"
echo "2. Start Flask REST API"
echo "3. Install dependencies only"
echo "4. Exit"
echo ""

read -p "Enter your choice (1-4): " choice

case $choice in
    1)
        echo "Starting Streamlit application..."
        cd streamlit_app
        streamlit run app.py
        ;;
    2)
        echo "Starting Flask API..."
        cd flask_api
        python app.py
        ;;
    3)
        echo "Dependencies installed!"
        ;;
    4)
        echo "Goodbye!"
        exit 0
        ;;
    *)
        echo "Invalid choice. Please run the script again."
        exit 1
        ;;
esac