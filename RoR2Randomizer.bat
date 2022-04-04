@echo off
echo "Activating python virtual environment..."
call .venv/Scripts/activate.bat
echo "Activated!"
echo "Starting the application..."
start /min pyw src/RoR2Randomizer.py
