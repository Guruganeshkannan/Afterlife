@echo off
echo Starting After Life Message Platform...

REM Check if Node.js is installed
where node >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo Node.js is not installed or not in PATH.
    echo Please install Node.js from https://nodejs.org/
    pause
    exit /b 1
)

REM Check if npm is installed
where npm >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo npm is not installed or not in PATH.
    echo Please install Node.js from https://nodejs.org/
    pause
    exit /b 1
)

REM Start the backend server in a new window
start cmd /k "python setup_and_run_backend.py"

REM Wait a moment for the backend to start
timeout /t 5

REM Start the frontend server in a new window
start cmd /k "python run_frontend.py"

echo Servers are starting in separate windows.
echo Backend will be available at http://localhost:8000
echo Frontend will be available at http://localhost:3000 