@echo off
echo "Installing..."
py -m venv .venv
echo "Installed!"
echo "Activating python virtual environment..."
call .venv/Scripts/activate.bat
echo "Activated!"
echo "Installing dependencies..."
pip install -r requirements.txt
echo "Installed!"
echo "You can now run the application"

pause
