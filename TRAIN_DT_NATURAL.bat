@echo off
setlocal
cd /d "%~dp0"

echo =============================================
echo DT lll - Natural Assistant Training
 echo DT-owned weights only
echo =============================================
echo.

if not exist ".venv\Scripts\python.exe" (
    echo ERROR: Python environment not found.
    echo Run:
    echo   py -3.11 -m venv .venv
    echo   .venv\Scripts\python.exe -m pip install -r model\requirements.txt
    pause
    exit /b 1
)

if not exist "data\dt_natural_ai_train.jsonl" (
    echo Creating the DT natural-assistant curriculum...
    ".venv\Scripts\python.exe" model\generate_dt_natural_curriculum.py
)

set OMP_NUM_THREADS=2
set MKL_NUM_THREADS=2
set CHECKPOINT=checkpoints\dt-lll-natural-3m.pt
set TARGET_STEPS=15000

if exist "%CHECKPOINT%" (
    echo Resuming DT natural training until step %TARGET_STEPS%...
    copy "%CHECKPOINT%" "checkpoints\dt-lll-natural-backup.pt" >nul
    ".venv\Scripts\python.exe" model\train.py --data data\dt_natural_ai_train.jsonl --out "%CHECKPOINT%" --resume "%CHECKPOINT%" --steps %TARGET_STEPS% --batch-size 1 --device cpu --d-model 256 --n-heads 8 --n-layers 4 --d-ff 1024
) else (
    echo Starting DT natural training until step %TARGET_STEPS%...
    ".venv\Scripts\python.exe" model\train.py --data data\dt_natural_ai_train.jsonl --out "%CHECKPOINT%" --steps %TARGET_STEPS% --batch-size 1 --device cpu --d-model 256 --n-heads 8 --n-layers 4 --d-ff 1024
)

if errorlevel 1 (
    echo Training failed. Copy the complete error above for troubleshooting.
    pause
    exit /b 1
)

echo.
echo DT natural training finished.
echo Checkpoint: %CHECKPOINT%
echo Test with:
echo .venv\Scripts\python.exe model\infer.py --checkpoint %CHECKPOINT% --prompt "Have a friendly conversation with me."
pause
