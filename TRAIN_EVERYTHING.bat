@echo off
setlocal
cd /d "%~dp0"

echo =============================================
echo DT lll - Overall Training
 echo Math + Java + English + Conversation
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

if not exist "data\beast_curriculum_train.jsonl" (
    echo ERROR: Math and Java dataset is missing.
    pause
    exit /b 1
)

if not exist "data\english_communication_train.jsonl" (
    echo ERROR: English dataset is missing.
    pause
    exit /b 1
)

if not exist "data\all_curriculum_train.jsonl" (
    echo Combining all training data into one file...
    type "data\beast_curriculum_train.jsonl" > "data\all_curriculum_train.jsonl"
    type "data\english_communication_train.jsonl" >> "data\all_curriculum_train.jsonl"
)

set OMP_NUM_THREADS=2
set MKL_NUM_THREADS=2
set CHECKPOINT=checkpoints\dt-lll-everything-3m.pt
set TARGET_STEPS=10000

if exist "%CHECKPOINT%" (
    echo Resuming the overall model until step %TARGET_STEPS%...
    copy "%CHECKPOINT%" "checkpoints\dt-lll-everything-backup.pt" >nul
    ".venv\Scripts\python.exe" model\train.py --data data\all_curriculum_train.jsonl --out "%CHECKPOINT%" --resume "%CHECKPOINT%" --steps %TARGET_STEPS% --batch-size 1 --device cpu --d-model 256 --n-heads 8 --n-layers 4 --d-ff 1024
) else (
    echo Starting the overall model until step %TARGET_STEPS%...
    ".venv\Scripts\python.exe" model\train.py --data data\all_curriculum_train.jsonl --out "%CHECKPOINT%" --steps %TARGET_STEPS% --batch-size 1 --device cpu --d-model 256 --n-heads 8 --n-layers 4 --d-ff 1024
)

if errorlevel 1 (
    echo.
    echo Training failed. Copy the complete error above for troubleshooting.
    pause
    exit /b 1
)

echo.
echo Overall training finished.
echo Model: %CHECKPOINT%
echo Test math:
echo .venv\Scripts\python.exe model\infer.py --checkpoint %CHECKPOINT% --prompt "Solve 11x + 22 = 99 step by step."
echo Test English:
echo .venv\Scripts\python.exe model\infer.py --checkpoint %CHECKPOINT% --prompt "Please explain this clearly in simple English."
echo Test Java:
echo .venv\Scripts\python.exe model\infer.py --checkpoint %CHECKPOINT% --prompt "Write a Java loop that prints 1 to 5."
pause
