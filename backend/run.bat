@echo off
set PYTHONPATH=%PYTHONPATH%;%CD%
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000 --workers 1 