# DT lll live website + local model

The static site now talks to the real DT lll checkpoint through `server.py`. It no longer uses canned browser replies.

## Start

From the project root:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r model/requirements.txt
python3 server.py
```

Open `http://127.0.0.1:8000`.

On Windows PowerShell:

```powershell
.venv\\Scripts\\Activate.ps1
pip install -r model\\requirements.txt
python server.py
```

## What works in the website

The chat panel sends prompts to `POST /api/chat`, which loads `checkpoints/dt-lll-14m.pt` and runs CPU inference. The Train panel calls `POST /api/train`, starts the real PyTorch training script in the background, and polls `GET /api/status` for the latest checkpoint step, loss, and log output. The Stop button calls `POST /api/train/stop`.

The server binds to `127.0.0.1` by default on purpose. Training control is not authenticated, so do not expose this server to the public internet. For a public deployment, add authentication and a process manager, or keep the static site public while running the model API only on your own computer.
