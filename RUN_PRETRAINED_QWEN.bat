@echo off
setlocal
cd /d "%~dp0"

echo =============================================
echo DT lll - Pretrained Qwen CPU Backend
echo =============================================
echo.

where llama >nul 2>nul
if errorlevel 1 (
    echo llama.cpp was not found.
    echo Install it from an Administrator PowerShell with:
    echo   winget install llama.cpp
    echo Then run this file again.
    pause
    exit /b 1
)

if not exist ".venv\Scripts\python.exe" (
    echo ERROR: Python environment not found.
    echo Run:
    echo   py -3.11 -m venv .venv
    echo   .venv\Scripts\python.exe -m pip install -r model\requirements.txt
    pause
    exit /b 1
)

echo Starting Qwen2.5 0.5B Instruct Q4_K_M on CPU...
start "DT lll Qwen backend" cmd /k "llama serve -hf Qwen/Qwen2.5-0.5B-Instruct-GGUF:Q4_K_M --host 127.0.0.1 --port 8080"

echo Waiting for the model server...
timeout /t 8 /nobreak >nul

echo Starting the DT lll website proxy...
.venv\Scripts\python.exe server_pretrained.py
