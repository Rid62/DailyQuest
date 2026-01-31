#!/usr/bin/env python3
"""Reset the database completely"""
import os
import sys
import time
import subprocess

# Path to the database
db_path = 'app.db'

# Kill any existing Flask/Python processes
print("Killing existing processes...")
os.system('taskkill /F /IM python.exe 2>nul')
time.sleep(2)

# Try to delete the database file
print(f"Deleting {db_path}...")
try:
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"✓ Deleted {db_path}")
    else:
        print(f"✓ {db_path} does not exist")
except Exception as e:
    print(f"✗ Error deleting {db_path}: {e}")
    sys.exit(1)

# Also delete dailyquest.db if it exists
if os.path.exists('dailyquest.db'):
    try:
        os.remove('dailyquest.db')
        print("✓ Deleted dailyquest.db")
    except:
        pass

# Start Flask
print("\nStarting Flask server...")
os.system('python app.py')
