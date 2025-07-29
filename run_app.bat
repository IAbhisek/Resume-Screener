@echo off
echo Starting Resume Screening Application...

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed or not in PATH. Please install Python 3.6 or higher.
    pause
    exit /b
)

:: Check if requirements are installed
echo Checking and installing requirements...
pip install -r requirements.txt

:: Run the application
echo Starting application...
python app.py

pause