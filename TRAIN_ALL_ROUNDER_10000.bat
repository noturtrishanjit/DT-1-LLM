@echo off
setlocal
cd /d "%~dp0"

echo =============================================
echo DT lll - 10,000-Step All-Rounder Training
echo English + Math + Java + Science + Indian History
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

if not exist "data\all_subjects_train.jsonl" (
    echo Creating the all-subjects training file...
    if not exist "data\science_indian_history_train.jsonl" (
        ".venv\Scripts\python.exe" model\generate_science_india_curriculum.py
    )
    type "data\beast_curriculum_train.jsonl" > "data\all_subjects_train.jsonl"
    type "data\english_communication_train.jsonl" >> "data\all_subjects_train.jsonl"
    type "data\science_indian_history_train.jsonl" >> "data\all_subjects_train.jsonl"
)

set OMP_NUM_THREADS=2
set MKL_NUM_THREADS=2
set CHECKPOINT=checkpoints\dt-lll-all-rounder-3m.pt
set TARGET_STEPS=10000

if exist "%CHECKPOINT%" (
    echo Resuming the all-rounder model until step %TARGET_STEPS%...
    copy "%CHECKPOINT%" "checkpoints\dt-lll-all-rounder-backup.pt" >nul
    ".venv\Scripts\python.exe" model\train.py --data data\all_subjects_train.jsonl --out "%CHECKPOINT%" --resume "%CHECKPOINT%" --steps %TARGET_STEPS% --batch-size 1 --device cpu --d-model 256 --n-heads 8 --n-layers 4 --d-ff 1024
) else (
    echo Starting a new all-rounder model until step %TARGET_STEPS%...
    ".venv\Scripts\python.exe" model\train.py --data data\all_subjects_train.jsonl --out "%CHECKPOINT%" --steps %TARGET_STEPS% --batch-size 1 --device cpu --d-model 256 --n-heads 8 --n-layers 4 --d-ff 1024
)

if errorlevel 1 (
    echo.
    echo Training failed. Copy the complete error above for troubleshooting.
    pause
    exit /b 1
)

echo.
echo All-rounder training finished at step 10000.
echo Checkpoint: %CHECKPOINT%
echo.
echo Test with:
echo .venv\Scripts\python.exe model\infer.py --checkpoint %CHECKPOINT% --prompt "Have a friendly conversation with me."
echo .venv\Scripts\python.exe model\infer.py --checkpoint %CHECKPOINT% --prompt "Explain photosynthesis simply."
echo .venv\Scripts\python.exe model\infer.py --checkpoint %CHECKPOINT% --prompt "Solve 11x + 22 = 99 step by step."
echo .venv\Scripts\python.exe model\infer.py --checkpoint %CHECKPOINT% --prompt "Write a Java loop that prints 1 to 5."
echo .venv\Scripts\python.exe model\infer.py --checkpoint %CHECKPOINT% --prompt "When did India become independent?"
pause
