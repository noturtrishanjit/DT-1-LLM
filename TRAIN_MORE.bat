@echo off
setlocal
cd /d "%~dp0"

echo =============================================
echo DT lll - More Training Launcher
echo =============================================
echo.

if not exist ".venv\Scripts\python.exe" (
    echo ERROR: Python environment not found.
    echo First run:
    echo   py -3.11 -m venv .venv
    echo   .venv\Scripts\python.exe -m pip install -r model\requirements.txt
    pause
    exit /b 1
)

if not exist "data\beast_curriculum_train.jsonl" (
    echo ERROR: Beast training data not found:
    echo   data\beast_curriculum_train.jsonl
    pause
    exit /b 1
)

set OMP_NUM_THREADS=2
set MKL_NUM_THREADS=2
set TARGET_STEPS=5000
set CHECKPOINT=checkpoints\dt-lll-beast-3m.pt

if exist "%CHECKPOINT%" (
    echo Resuming existing model until step %TARGET_STEPS%...
    ".venv\Scripts\python.exe" model\train.py ^
      --data data\beast_curriculum_train.jsonl ^
      --out "%CHECKPOINT%" ^
      --resume "%CHECKPOINT%" ^
      --steps %TARGET_STEPS% ^
      --batch-size 1 ^
      --device cpu ^
      --d-model 256 --n-heads 8 --n-layers 4 --d-ff 1024
) else (
    echo Starting a new 3.35M model until step %TARGET_STEPS%...
    ".venv\Scripts\python.exe" model\train.py ^
      --data data\beast_curriculum_train.jsonl ^
      --out "%CHECKPOINT%" ^
      --steps %TARGET_STEPS% ^
      --batch-size 1 ^
      --device cpu ^
      --d-model 256 --n-heads 8 --n-layers 4 --d-ff 1024
)

if errorlevel 1 (
    echo.
    echo Training failed. Copy the complete error above for troubleshooting.
    pause
    exit /b 1
)

echo.
echo Training finished. Test the model with:
echo .venv\Scripts\python.exe model\infer.py --checkpoint %CHECKPOINT% --prompt "Solve 11x + 22 = 99 step by step."
pause
