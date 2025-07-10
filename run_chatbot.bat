@echo off
echo Starting Medical Chatbot...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed or not in PATH
    echo Please install Python 3.8 or higher
    pause
    exit /b 1
)

REM Check if pip is available
pip --version >nul 2>&1
if errorlevel 1 (
    echo pip is not available
    echo Please make sure pip is installed
    pause
    exit /b 1
)

REM Install requirements if they don't exist
echo Installing required packages...
pip install -r requirements.txt

REM Check if installation was successful
if errorlevel 1 (
    echo Failed to install requirements
    pause
    exit /b 1
)

echo.
echo Starting Flask server...
echo The chatbot will be available at: http://localhost:5000
echo Press Ctrl+C to stop the server
echo.

REM Start the Flask application
python app.py

pause
