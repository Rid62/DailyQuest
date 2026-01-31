@echo off
REM DailyQuest - Windows Setup Script
REM This script sets up the DailyQuest application

echo.
echo ============================================
echo    DailyQuest - Setup Script (Windows)
echo ============================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo [✓] Python found
echo.

REM Create virtual environment
echo [1] Creating virtual environment...
if exist venv (
    echo Virtual environment already exists. Skipping...
) else (
    python -m venv venv
    echo [✓] Virtual environment created
)
echo.

REM Activate virtual environment
echo [2] Activating virtual environment...
call venv\Scripts\activate.bat
echo [✓] Virtual environment activated
echo.

REM Install dependencies
echo [3] Installing dependencies...
pip install -r requirements.txt
echo [✓] Dependencies installed
echo.

REM Run the application
echo [4] Starting DailyQuest application...
echo.
echo ============================================
echo    DailyQuest is running!
echo ============================================
echo.
echo Open your browser and go to:
echo    http://localhost:5000
echo.
echo Register a new account to get started!
echo Press Ctrl+C to stop the server.
echo.

python app.py

pause
