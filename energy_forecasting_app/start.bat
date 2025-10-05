@echo off
REM Energy Forecasting Application Launcher for Windows
REM This batch script helps you quickly start either the Streamlit app or Flask API

echo ⚡ Energy Forecasting Application Launcher
echo ==========================================
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

REM Install requirements if needed
echo 📥 Installing/updating requirements...
pip install -r requirements.txt

echo.
echo Choose an option:
echo 1. Start Streamlit Web App
echo 2. Start Flask REST API
echo 3. Install dependencies only
echo 4. Exit
echo.

set /p choice="Enter your choice (1-4): "

if "%choice%"=="1" (
    echo 🚀 Starting Streamlit application...
    cd streamlit_app
    streamlit run app.py
) else if "%choice%"=="2" (
    echo 🚀 Starting Flask API...
    cd flask_api
    python app.py
) else if "%choice%"=="3" (
    echo ✅ Dependencies installed!
    pause
) else if "%choice%"=="4" (
    echo 👋 Goodbye!
    exit /b 0
) else (
    echo ❌ Invalid choice. Please run the script again.
    pause
    exit /b 1
)