# Run the saved DT lll 14M model

This package contains a saved CPU checkpoint at `checkpoints/dt-lll-14m.pt`.

## Install

```bash
python3 -m venv .venv
# Linux/macOS
source .venv/bin/activate
# Windows PowerShell: .venv\\Scripts\\Activate.ps1
pip install -r model/requirements.txt
```

## CPU inference

```bash
python3 model/infer.py \
  --checkpoint checkpoints/dt-lll-14m.pt \
  --prompt "Solve 7x - 14 = 35 step by step."
```

For lower memory usage, use dynamic INT8 quantization:

```bash
python3 model/infer.py \
  --checkpoint checkpoints/dt-lll-14m.pt \
  --prompt "Write a Java loop that prints 1 to 7." \
  --quantize int8
```

## Continue training

The 14M architecture is 8 layers, 384 hidden dimensions, 6 attention heads, and 1,536-dimensional feed-forward layers. The last saved checkpoint may be resumed with:

```bash
python3 model/train.py \
  --data data/curriculum_train.jsonl \
  --out checkpoints/dt-lll-14m.pt \
  --resume checkpoints/dt-lll-14m.pt \
  --steps 2000 \
  --batch-size 8 \
  --device cpu \
  --d-model 384 --n-heads 6 --n-layers 8 --d-ff 1536
```

`--steps` is the final step number, not an additional-step count. CPU training is slow; a GPU is recommended for substantial continuation.

## Important limitation

This checkpoint was trained on a small synthetic task-focused corpus. It is a stronger demonstration model, not a general Claude-class model. Add a large, licensed, high-quality dataset before making claims about broad capability.
