# Checkpoints

Model weights are intentionally not committed to the public source repository by default.

To create a checkpoint locally, follow the training instructions in the root `README.md` and run:

```bash
python model/generate_dt_natural_curriculum.py
python model/train.py \
  --data data/dt_natural_ai_train.jsonl \
  --out checkpoints/dt-lll-natural-3m.pt \
  --steps 15000 --batch-size 1 --device cpu \
  --d-model 256 --n-heads 8 --n-layers 4 --d-ff 1024
```

If you publish weights separately, document the exact training commit, dataset version, checksum, model configuration, and license/usage terms. Do not commit private, restricted, or accidentally collected data.
