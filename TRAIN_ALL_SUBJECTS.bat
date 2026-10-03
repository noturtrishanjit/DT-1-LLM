@echo off
setlocal
cd /d "%~dp0"

echo =============================================
echo DT lll - All Subjects Training
echo Math + Java + English + Science + Indian History
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
if not exist "data\science_indian_history_train.jsonl" (
    echo Creating science and Indian-history data...
    ".venv\Scripts\python.exe" model\generate_science_india_curriculum.py
)

if not exist "data\all_subjects_train.jsonl" (
    echo Combining all subjects into one training file...
    type "data\beast_curriculum_train.jsonl" > "data\all_subjects_train.jsonl"
    type "data\english_communication_train.jsonl" >> "data\all_subjects_train.jsonl"
    type "data\science_indian_history_train.jsonl" >> "data\all_subjects_train.jsonl"
)

set OMP_NUM_THREADS=2
set MKL_NUM_THREADS=2
set CHECKPOINT=checkpoints\dt-lll-all-subjects-3m.pt
set TARGET_STEPS=15000

if exist "%CHECKPOINT%" (
    echo Resuming all-subjects training until step %TARGET_STEPS%...
    copy "%CHECKPOINT%" "checkpoints\dt-lll-all-subjects-backup.pt" >nul
    ".venv\Scripts\python.exe" model\train.py --data data\all_subjects_train.jsonl --out "%CHECKPOINT%" --resume "%CHECKPOINT%" --steps %TARGET_STEPS% --batch-size 1 --device cpu --d-model 256 --n-heads 8 --n-layers 4 --d-ff 1024
) else (
    echo Starting all-subjects training until step %TARGET_STEPS%...
    ".venv\Scripts\python.exe" model\train.py --data data\all_subjects_train.jsonl --out "%CHECKPOINT%" --steps %TARGET_STEPS% --batch-size 1 --device cpu --d-model 256 --n-heads 8 --n-layers 4 --d-ff 1024
)

if errorlevel 1 (
    echo.
    echo Training failed. Copy the complete error above for troubleshooting.
    pause
    exit /b 1
)

echo.
echo All-subjects training finished.
echo Model: %CHECKPOINT%
echo Test English:
echo .venv\Scripts\python.exe model\infer.py --checkpoint %CHECKPOINT% --prompt "Explain photosynthesis in simple English."
echo Test science:
echo .venv\Scripts\python.exe model\infer.py --checkpoint %CHECKPOINT% --prompt "What is gravity?"
echo Test Indian history:
echo .venv\Scripts\python.exe model\infer.py --checkpoint %CHECKPOINT% --prompt "When did India become independent?"
echo Test math:
echo .venv\Scripts\python.exe model\infer.py --checkpoint %CHECKPOINT% --prompt "Solve 11x + 22 = 99 step by step."
echo Test Java:
echo .venv\Scripts\python.exe model\infer.py --checkpoint %CHECKPOINT% --prompt "Write a Java loop that prints 1 to 5."
pause
