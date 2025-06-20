@echo off
echo Stopping any running uvicorn processes...
taskkill /F /IM uvicorn.exe /T 2>nul

echo Removing existing python-jose installation...
pip uninstall -y python-jose

echo Installing dependencies...
pip install --upgrade pip
pip install -r requirements.txt

echo Setup complete!
pause 