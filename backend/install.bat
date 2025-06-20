@echo off
echo Installing AfterLife Message Platform...

:: Stop any running uvicorn processes
echo Stopping any running uvicorn processes...
taskkill /F /IM uvicorn.exe /T 2>nul

:: Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

:: Uninstall problematic packages
echo Removing existing packages...
pip uninstall -y python-jose PyJWT fastapi-mail python-dotenv

:: Install requirements
echo Installing requirements...
pip install -r requirements.txt

:: Install the package in development mode
echo Installing package in development mode...
pip install -e .

echo Installation complete!
echo.
echo To test email functionality, run: python direct_email_test.py
pause 