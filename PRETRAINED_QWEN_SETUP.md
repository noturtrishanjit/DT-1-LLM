# DT lll with a pretrained CPU model

## Why this option exists

The custom 3.35M DT lll checkpoint is useful as a learning project, but it cannot behave like a normal large assistant. This option keeps your DT lll website and personality while using a pretrained instruction model for much stronger general conversation.

The selected model is **Qwen2.5-0.5B-Instruct-GGUF Q4_K_M**. The official model page lists an Apache-2.0 license and a Q4_K_M file of approximately 491MB. It runs with llama.cpp on CPU and does not require CUDA.

## Windows 10 setup

Open **Administrator PowerShell once** only for installing llama.cpp:

```powershell
winget install llama.cpp
```

Close that window after installation. Normal Command Prompt is sufficient afterward.

Inside the extracted `dt-lll` project folder, create/install the Python environment if you have not already:

```bat
cd /d "D:\dt-lll"
py -3.11 -m venv .venv
.venv\Scripts\python.exe -m pip install -r model\requirements.txt
```

## Start the pretrained website

Double-click:

```text
RUN_PRETRAINED_QWEN.bat
```

The first run downloads the Q4_K_M model. This may take time and requires internet access. Later runs reuse the local model cache.

The launcher opens two windows:

1. The llama.cpp model server on `127.0.0.1:8080`.
2. The DT lll website proxy on `127.0.0.1:8000`.

Open Chrome or Edge:

```text
http://127.0.0.1:8000
```

The chat now uses the pretrained Qwen model, not the tiny DT lll checkpoint and not a simulated response.

## Test the backend directly

With both windows running:

```bat
curl http://127.0.0.1:8080/health
```

Then test the DT lll website API:

```bat
curl -X POST http://127.0.0.1:8000/api/chat -H "Content-Type: application/json" -d "{\"prompt\":\"Explain gravity in simple English.\"}"
```

## Stop it

Close the website proxy Command Prompt with `Ctrl+C`. Close the llama.cpp window afterward.

## Relationship to your custom model

- `server.py` still runs your custom DT lll checkpoint and training controls.
- `RUN_PRETRAINED_QWEN.bat` runs the stronger pretrained conversational backend.
- The Qwen model is not trained from scratch on your dataset by this launcher.
- Your DT lll datasets can later be used for retrieval, prompt examples, or fine-tuning on stronger hardware.

## Hardware expectation

Q4_K_M is roughly 491MB for the model file, but runtime memory is higher. CPU generation will be slower than a cloud model, especially on an older laptop. The Intel HD Graphics 520 is not used for CUDA training; llama.cpp will run primarily on the CPU.
