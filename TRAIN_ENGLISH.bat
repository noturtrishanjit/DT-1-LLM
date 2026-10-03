@echo off
setlocal
cd /d "%~dp0"

echo =============================================
echo DT lll - English Communication Training
echo =============================================
echo.

if not exist ".venv\Scripts\python.exe" (
    echo ERROR: Python environment not found.
    echo Run: py -3.11 -m venv .venv
    echo Then: .venv\Scripts\python.exe -m pip install -r model\requirements.txt
    pause
    exit /b 1
)

if not exist "data\english_communication_train.jsonl" (
    echo Creating the English communication dataset...
    ".venv\Scripts\python.exe" model\generate_english_curriculum.py
)

set OMP_NUM_THREADS=2
set MKL_NUM_THREADS=2
set TARGET_STEPS=5000
set CHECKPOINT=checkpoints\dt-lll-english-3m.pt

if exist "%CHECKPOINT%" (
    echo Resuming English training until step %TARGET_STEPS%...
    ".venv\Scripts\python.exe" model\train.py --data data\english_communication_train.jsonl --out "%CHECKPOINT%" --resume "%CHECKPOINT%" --steps %TARGET_STEPS% --batch-size 1 --device cpu --d-model 256 --n-heads 8 --n-layers 4 --d-ff 1024
) else (
    echo Starting English training until step %TARGET_STEPS%...
    ".venv\Scripts\python.exe" model\train.py --data data\english_communication_train.jsonl --out "%CHECKPOINT%" --steps %TARGET_STEPS% --batch-size 1 --device cpu --d-model 256 --n-heads 8 --n-layers 4 --d-ff 1024
)

if errorlevel 1 (
    echo Training failed. Copy the complete error above for troubleshooting.
    pause
    exit /b 1
)

echo.
echo Training finished. Test with:
echo .venv\Scripts\python.exe model\infer.py --checkpoint %CHECKPOINT% --prompt "Please explain this clearly."
pause
