@echo off

REM Banking Management System - Quick Start Script for Windows

echo.
echo 0x26C5 Banking Management System
echo =====================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo X Python is not installed. Please install Python 3.8 or higher.
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo + Python found: %PYTHON_VERSION%
echo.

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo X Failed to install dependencies
    pause
    exit /b 1
)

echo + Dependencies installed
echo.

REM Start the application
echo Starting application...
echo.
echo Access the application at: http://localhost:5000
echo.
echo Default Admin:
echo   Username: admin
echo   Password: password
echo.
echo Press Ctrl+C to stop the server
echo.

python app.py
pause
