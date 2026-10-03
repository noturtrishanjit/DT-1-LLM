#!/usr/bin/env bash
set -euo pipefail
PROMPT="${*:-Explain what a Java for loop does.}"
python3 model/infer.py --checkpoint checkpoints/dt-lll-14m.pt --prompt "$PROMPT" --quantize int8
