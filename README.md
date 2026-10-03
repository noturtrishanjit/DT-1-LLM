# DT lll

> A tiny, CPU-first language-model experiment for conversation, student math, beginner Java, science, and Indian history.

**DT lll is an educational open-source project—not a Claude- or ChatGPT-class model.** It is designed to make the complete path from training data to a local browser chat understandable and runnable on ordinary computers.

Project owner: [@noturtrishanjit](https://github.com/noturtrishanjit)

## What is included

- A small decoder-only Transformer written in PyTorch
- A deterministic UTF-8 byte tokenizer
- CPU training and inference scripts
- Optional PyTorch dynamic INT8 inference
- Natural-assistant, math, Java, science, English, and Indian-history curricula
- A local Flask API that runs the real DT checkpoint
- A dedicated responsive browser workspace
- Windows `.bat` launchers and Linux/macOS shell launchers
- An optional Qwen/llama.cpp backend documented separately for stronger local conversation

## Honest limitations

The custom DT lll model is small. It can learn the style and patterns in its training data, but it has limited factual memory, weak long-context behavior, and unreliable complex reasoning. It may produce incorrect math, code, science, or history answers.

Do not use it as the sole authority for medical, legal, financial, security-critical, or production decisions. Verify important answers.

The custom DT lll checkpoint is a PyTorch `.pt` file. It is **not directly convertible to a runnable GGUF file** because its custom architecture and byte tokenizer are not supported by standard `llama.cpp` loaders.

## Architecture

The default small configuration is:

| Component | Value |
|---|---:|
| Transformer type | Decoder-only causal Transformer |
| Layers | 4 |
| Hidden size | 256 |
| Attention heads | 8 |
| Feed-forward size | 1,024 |
| Context length | 512 tokens |
| Vocabulary | 259 UTF-8 byte/special-token IDs |
| Approximate parameters | 3.35M |

A larger historical checkpoint may also exist locally, but checkpoints are intentionally excluded from Git by default.

## Quickstart

### Windows 10/11

Install Python 3.11 64-bit, then open Command Prompt in the repository folder:

```bat
py -3.11 -m venv .venv
.venv\Scripts\python.exe -m pip install -r model\requirements.txt
```

Run a terminal prompt using a checkpoint placed in `checkpoints\`:

```bat
.venv\Scripts\python.exe model\infer.py --checkpoint checkpoints\dt-lll-natural-3m.pt --prompt "Have a friendly conversation with me."
```

Start the pure DT lll browser app:

```bat
RUN_DT_APP.bat
```

Then open the URL printed by the server, normally:

```text
http://127.0.0.1:8000/app.html
```

Do not open `website\app.html` directly from File Explorer; the API needs the local HTTP server.

### Linux/macOS

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r model/requirements.txt
./run_server.sh
```

Open `http://127.0.0.1:8000/app.html`.

## Train DT lll from its own data

The natural-assistant curriculum is generated locally and contains original synthetic examples for turn-taking, follow-up questions, empathy, uncertainty, math, Java, science, and Indian history.

Generate it:

```bash
python model/generate_dt_natural_curriculum.py
```

Train the small custom DT model:

```bash
python model/train.py \
  --data data/dt_natural_ai_train.jsonl \
  --out checkpoints/dt-lll-natural-3m.pt \
  --steps 15000 \
  --batch-size 1 \
  --device cpu \
  --d-model 256 --n-heads 8 --n-layers 4 --d-ff 1024
```

On Windows, the same workflow is one command:

```bat
TRAIN_DT_NATURAL.bat
```

To resume, use a higher target step and the existing checkpoint:

```bash
python model/train.py \
  --data data/dt_natural_ai_train.jsonl \
  --out checkpoints/dt-lll-natural-3m.pt \
  --resume checkpoints/dt-lll-natural-3m.pt \
  --steps 20000 \
  --batch-size 1 --device cpu \
  --d-model 256 --n-heads 8 --n-layers 4 --d-ff 1024
```

## Evaluate

```bash
python model/evaluate.py \
  --checkpoint checkpoints/dt-lll-natural-3m.pt \
  --data data/dt_natural_ai_eval.jsonl
```

For Java, compile generated snippets with a local JDK. For math, test unseen values and verify the final answer. The included evaluator is a smoke test, not a benchmark.

## Dedicated local web app

Start the pure DT backend:

```bash
python server.py
```

Then open:

```text
http://127.0.0.1:8000/app.html
```

The app provides:

- Local chat history
- Prompt suggestions
- Conversation export
- Clear/new conversation controls
- Backend health status
- Response length and temperature controls

The browser talks to these local endpoints:

```text
GET  /api/health
GET  /api/status
POST /api/chat
POST /api/train
POST /api/train/stop
```

The training endpoints have no authentication. Keep the server bound to `127.0.0.1` and do not expose it to the public internet.

## Optional stronger local backend

`RUN_PRETRAINED_QWEN.bat` can run Qwen2.5-0.5B-Instruct through llama.cpp for stronger general conversation. That mode is **not the custom DT lll model**; it is an optional pretrained backend using the DT lll interface and system prompt.

Read [`PRETRAINED_QWEN_SETUP.md`](PRETRAINED_QWEN_SETUP.md) before using it. The Qwen model has its own license and attribution requirements.

## Repository structure

```text
DT lll/
├── data/                         # Small generated/example JSONL curricula
├── docs/                         # System prompt and supporting documentation
├── model/                        # Architecture, training, inference, evaluation
├── website/                      # Landing page and dedicated local app
├── checkpoints/                  # Local weights; ignored by Git by default
├── server.py                     # Pure DT lll local Flask API
├── server_pretrained.py          # Optional llama.cpp proxy
├── RUN_DT_APP.bat                # Windows pure-DT app launcher
├── TRAIN_DT_NATURAL.bat          # Windows DT-owned training launcher
├── RUN_PRETRAINED_QWEN.bat       # Optional pretrained backend launcher
├── model/requirements.txt        # Python dependencies
└── README.md
```

## Data and licensing

The included generated curricula are synthetic educational examples created for this project. If you add external datasets, check their licenses, retain attribution, and do not commit restricted or scraped data without permission.

This repository does not grant a license unless you add one. Choose a license before presenting the repository as reusable open-source software.

## Contributing

1. Create a branch.
2. Make a focused change.
3. Run Python syntax checks and the relevant smoke test.
4. Document dataset sources and licenses.
5. Open a pull request with what changed and how it was tested.

## Roadmap

- Replace the byte tokenizer with a trained BPE/SentencePiece tokenizer.
- Add a larger, properly licensed pretraining corpus.
- Add held-out conversation and subject evaluations.
- Add Java compilation tests and math exact-match tests.
- Design a llama.cpp-compatible architecture if a future GGUF release is needed.
