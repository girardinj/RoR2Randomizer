@echo off
echo Activating python virtual environment...
call .venv/Scripts/activate.bat
echo Activated!
echo Starting the application...
cd ./src/
start /min pyw ./RoR2Randomizer.py
