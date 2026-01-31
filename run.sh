#!/bin/bash
# DailyQuest - macOS/Linux Setup Script

echo ""
echo "============================================"
echo "    DailyQuest - Setup Script (macOS/Linux)"
echo "============================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python from https://www.python.org"
    exit 1
fi

echo "[✓] Python found"
echo ""

# Create virtual environment
echo "[1] Creating virtual environment..."
if [ -d "venv" ]; then
    echo "Virtual environment already exists. Skipping..."
else
    python3 -m venv venv
    echo "[✓] Virtual environment created"
fi
echo ""

# Activate virtual environment
echo "[2] Activating virtual environment..."
source venv/bin/activate
echo "[✓] Virtual environment activated"
echo ""

# Install dependencies
echo "[3] Installing dependencies..."
pip install -r requirements.txt
echo "[✓] Dependencies installed"
echo ""

# Run the application
echo "[4] Starting DailyQuest application..."
echo ""
echo "============================================"
echo "    DailyQuest is running!"
echo "============================================"
echo ""
echo "Open your browser and go to:"
echo "    http://localhost:5000"
echo ""
echo "Register a new account to get started!"
echo "Press Ctrl+C to stop the server."
echo ""

python3 app.py
