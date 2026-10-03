@echo off
set PROMPT=%*
if "%PROMPT%"=="" set PROMPT=Explain what a Java for loop does.
python model\infer.py --checkpoint checkpoints\dt-lll-14m.pt --prompt "%PROMPT%" --quantize int8
