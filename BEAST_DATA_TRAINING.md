# DT lll beast curriculum training guide

## What this file is

`data/beast_curriculum_train.jsonl` contains **16,200 synthetic, license-free records** and is approximately 3.2MB.

The distribution is:

| Category | Records |
|---|---:|
| Arithmetic, percentages, fractions, algebra, word problems | 10,900 |
| Java loops, conditions, methods, arrays, debugging | 3,500 |
| Conversation and study help | 1,800 |

It is much broader than the original three examples, but it is still synthetic template data. It teaches task patterns; it does not provide broad factual knowledge like a large web-scale corpus.

## Windows potato-PC training

Open PowerShell in the project folder:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
py -3.11 -m venv .venv
.venv\\Scripts\\Activate.ps1
pip install -r model\\requirements.txt
```

Limit CPU usage so the computer remains usable:

```powershell
$env:OMP_NUM_THREADS="2"
$env:MKL_NUM_THREADS="2"
```

### First smoke test

Train the 3.35M model for 100 steps:

```powershell
python model\\train.py --data data\\beast_curriculum_train.jsonl --out checkpoints\\dt-lll-beast-3m.pt --steps 100 --batch-size 1 --device cpu --d-model 256 --n-heads 8 --n-layers 4 --d-ff 1024
```

### Useful potato-PC run

```powershell
python model\\train.py --data data\\beast_curriculum_train.jsonl --out checkpoints\\dt-lll-beast-3m.pt --steps 2000 --batch-size 1 --device cpu --d-model 256 --n-heads 8 --n-layers 4 --d-ff 1024
```

### Longer run

```powershell
python model\\train.py --data data\\beast_curriculum_train.jsonl --out checkpoints\\dt-lll-beast-3m.pt --steps 10000 --batch-size 1 --device cpu --d-model 256 --n-heads 8 --n-layers 4 --d-ff 1024
```

Training time depends heavily on the CPU. Start with 100 steps first. A 10,000-step CPU run can take many hours on a low-end computer.

## Linux/macOS commands

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r model/requirements.txt
export OMP_NUM_THREADS=2
export MKL_NUM_THREADS=2
python model/train.py --data data/beast_curriculum_train.jsonl --out checkpoints/dt-lll-beast-3m.pt --steps 2000 --batch-size 1 --device cpu --d-model 256 --n-heads 8 --n-layers 4 --d-ff 1024
```

## Continue training

If training reaches step 2,000, continue to step 10,000:

```powershell
python model\\train.py --data data\\beast_curriculum_train.jsonl --out checkpoints\\dt-lll-beast-3m.pt --resume checkpoints\\dt-lll-beast-3m.pt --steps 10000 --batch-size 1 --device cpu --d-model 256 --n-heads 8 --n-layers 4 --d-ff 1024
```

The `--steps` value is the final target step. It is not an additional-step count.

## Test the result

```powershell
python model\\infer.py --checkpoint checkpoints\\dt-lll-beast-3m.pt --prompt "Solve 11x + 22 = 99 step by step."
python model\\infer.py --checkpoint checkpoints\\dt-lll-beast-3m.pt --prompt "Write Java code that checks whether 42 is even or odd." --quantize int8
```

Evaluate on held-out prompts:

```powershell
python model\\evaluate.py --checkpoint checkpoints\\dt-lll-beast-3m.pt --data data\\beast_curriculum_eval.jsonl
```

## Browser training

Start the local API:

```powershell
python server.py
```

Open `http://127.0.0.1:8000`. The browser Train panel now uses `data/beast_curriculum_train.jsonl` by default for the 14M checkpoint. For the potato 3M model, use the terminal command above.

## Honest expectation

This dataset is intentionally large for a tiny project, but it is not a magic “know everything” file. The model can improve at the covered formats while still failing unseen reasoning, factual questions, and complex math. Always evaluate on prompts that were not copied from the training file.
