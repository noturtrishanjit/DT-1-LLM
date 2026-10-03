@echo off
setlocal
cd /d "%~dp0"

echo =============================================
echo DT lll - English Training to Step 10000
echo =============================================
echo.

if not exist ".venv\Scripts\python.exe" (
    echo ERROR: Python environment not found.
    echo Run setup first:
    echo   py -3.11 -m venv .venv
    echo   .venv\Scripts\python.exe -m pip install -r model\requirements.txt
    pause
    exit /b 1
)

if not exist "data\english_communication_train.jsonl" (
    echo ERROR: English training data not found.
    pause
    exit /b 1
)

if not exist "checkpoints\dt-lll-english-3m.pt" (
    echo No English checkpoint found. Run TRAIN_ENGLISH.bat first.
    pause
    exit /b 1
)

set OMP_NUM_THREADS=2
set MKL_NUM_THREADS=2
set CHECKPOINT=checkpoints\dt-lll-english-3m.pt

copy "%CHECKPOINT%" "checkpoints\dt-lll-english-backup.pt" >nul

echo Resuming English training until step 10000...
".venv\Scripts\python.exe" model\train.py --data data\english_communication_train.jsonl --out "%CHECKPOINT%" --resume "%CHECKPOINT%" --steps 10000 --batch-size 1 --device cpu --d-model 256 --n-heads 8 --n-layers 4 --d-ff 1024

if errorlevel 1 (
    echo.
    echo Training failed. Your backup is:
    echo   checkpoints\dt-lll-english-backup.pt
    pause
    exit /b 1
)

echo.
echo Training finished through step 10000.
echo Test it with:
echo .venv\Scripts\python.exe model\infer.py --checkpoint %CHECKPOINT% --prompt "Please explain this clearly."
pause
