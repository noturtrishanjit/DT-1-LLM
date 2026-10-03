@echo off
setlocal
cd /d "%~dp0"

echo =============================================
echo DT lll Dedicated App - Pure DT Backend
echo =============================================
if not exist ".venv\Scripts\python.exe" (
    echo ERROR: Python environment not found.
    echo Run:
    echo   py -3.11 -m venv .venv
    echo   .venv\Scripts\python.exe -m pip install -r model\requirements.txt
    pause
    exit /b 1
)
if not exist "checkpoints\dt-lll-natural-3m.pt" if not exist "checkpoints\dt-lll-all-rounder-3m.pt" if not exist "checkpoints\dt-lll-14m.pt" (
    echo ERROR: No DT lll checkpoint was found in checkpoints\.
    echo Train a checkpoint first, then run this file again.
    pause
    exit /b 1
)
start "DT lll browser" cmd /c "timeout /t 2 /nobreak >nul & start http://127.0.0.1:8000/app.html"
echo Starting the pure DT lll server...
echo Keep this window open while using the app.
.venv\Scripts\python.exe server.py
pause
