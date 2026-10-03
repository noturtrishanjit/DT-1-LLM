"""Local DT lll web server.

Run from the project root: python3 server.py
The API intentionally binds to 127.0.0.1 by default because training controls
must not be exposed publicly without authentication.
"""
import json, os, subprocess, sys, threading
from pathlib import Path
from flask import Flask, jsonify, request, send_from_directory
import torch

ROOT = Path(__file__).resolve().parent
WEBSITE = ROOT / "website"
_checkpoint_candidates = [
    Path(os.getenv("DT_CHECKPOINT", "")) if os.getenv("DT_CHECKPOINT") else None,
    ROOT / "checkpoints" / "dt-lll-natural-3m.pt",
    ROOT / "checkpoints" / "dt-lll-all-rounder-3m.pt",
    ROOT / "checkpoints" / "dt-lll-14m.pt",
]
CHECKPOINT = next((p if p.is_absolute() else ROOT / p for p in _checkpoint_candidates if p and p.exists()), ROOT / "checkpoints" / "dt-lll-natural-3m.pt")
TRAIN_LOG = ROOT / "checkpoints" / "web-train.log"
MODEL_DIR = ROOT / "model"
sys.path.insert(0, str(MODEL_DIR))
from model import TinyTransformer  # noqa: E402

app = Flask(__name__, static_folder=str(WEBSITE), static_url_path="")
model_lock = threading.Lock()
model = None
tokenizer = None
checkpoint_mtime = None
train_process = None


def load_model(force=False):
    global model, tokenizer, checkpoint_mtime
    if not CHECKPOINT.exists():
        raise FileNotFoundError(f"Checkpoint not found: {CHECKPOINT}")
    mtime = CHECKPOINT.stat().st_mtime
    if force or model is None or checkpoint_mtime != mtime:
        with model_lock:
            if force or model is None or checkpoint_mtime != mtime:
                model, tokenizer, _ = TinyTransformer.from_checkpoint(str(CHECKPOINT), device="cpu")
                model.eval()
                checkpoint_mtime = mtime
    return model, tokenizer


def generate(prompt, max_new_tokens=160, temperature=0.65, top_k=40):
    net, tok = load_model()
    text = f"User: {prompt}\nAssistant:"
    ids = torch.tensor([tok.encode(text, add_eos=False)], dtype=torch.long)
    with model_lock, torch.no_grad():
        for _ in range(max(1, min(int(max_new_tokens), 320))):
            logits, _ = net(ids[:, -net.cfg.context_length:])
            logits = logits[:, -1, :] / max(float(temperature), 0.05)
            values, indices = torch.topk(logits, min(int(top_k), logits.shape[-1]))
            probs = torch.softmax(values, dim=-1)
            nxt = indices.gather(-1, torch.multinomial(probs, 1))
            ids = torch.cat([ids, nxt], dim=1)
            if nxt.item() == tok.EOS:
                break
    answer = tok.decode(ids[0].tolist()).split("Assistant:", 1)[-1].strip()
    return answer


def training_status():
    running = train_process is not None and train_process.poll() is None
    log = TRAIN_LOG.read_text(errors="replace")[-5000:] if TRAIN_LOG.exists() else ""
    return {"running": running, "pid": train_process.pid if running else None, "log": log}


@app.get("/api/health")
def health():
    return jsonify({"ok": True, "checkpoint": CHECKPOINT.exists(), "training": training_status()})


@app.post("/api/chat")
def chat():
    body = request.get_json(silent=True) or {}
    prompt = str(body.get("prompt", "")).strip()
    if not prompt:
        return jsonify({"error": "prompt is required"}), 400
    try:
        answer = generate(prompt, body.get("max_new_tokens", 160), body.get("temperature", 0.65))
        return jsonify({"answer": answer, "model": "dt-lll-14m", "simulated": False})
    except Exception as exc:
        return jsonify({"error": str(exc)}), 500


@app.get("/api/status")
def status():
    result = training_status()
    if CHECKPOINT.exists():
        try:
            ckpt = torch.load(CHECKPOINT, map_location="cpu", weights_only=False)
            result.update({"checkpoint": str(CHECKPOINT.relative_to(ROOT)), "step": ckpt.get("step"), "loss": ckpt.get("loss"), "config": ckpt.get("config")})
        except Exception as exc:
            result["checkpoint_error"] = str(exc)
    return jsonify(result)


@app.post("/api/train")
def train():
    global train_process
    if train_process is not None and train_process.poll() is None:
        return jsonify({"error": "training is already running", "pid": train_process.pid}), 409
    body = request.get_json(silent=True) or {}
    steps = max(1, min(int(body.get("steps", 1800)), 10000))
    if CHECKPOINT.exists():
        current = torch.load(CHECKPOINT, map_location="cpu", weights_only=False).get("step", 0)
        if steps <= current:
            return jsonify({"error": f"target step must be greater than current checkpoint step {current}"}), 400
    data = ROOT / "data" / "beast_curriculum_train.jsonl"
    if not data.exists():
        data = ROOT / "data" / "curriculum_train.jsonl"
    if not data.exists():
        return jsonify({"error": "training data not found"}), 400
    TRAIN_LOG.parent.mkdir(exist_ok=True)
    log_handle = TRAIN_LOG.open("w", encoding="utf-8")
    cmd = [sys.executable, str(MODEL_DIR / "train.py"), "--data", str(data), "--out", str(CHECKPOINT), "--steps", str(steps), "--batch-size", "8", "--device", "cpu", "--d-model", "384", "--n-heads", "6", "--n-layers", "8", "--d-ff", "1536"]
    if CHECKPOINT.exists():
        cmd += ["--resume", str(CHECKPOINT)]
    train_process = subprocess.Popen(cmd, cwd=ROOT, stdout=log_handle, stderr=subprocess.STDOUT, text=True)
    return jsonify({"started": True, "pid": train_process.pid, "steps": steps})


@app.post("/api/train/stop")
def stop_train():
    global train_process
    if train_process is None or train_process.poll() is not None:
        return jsonify({"stopped": False, "message": "no training process is running"})
    train_process.terminate()
    return jsonify({"stopped": True, "pid": train_process.pid})


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def website(path):
    target = WEBSITE / path
    if path and target.is_file():
        return send_from_directory(WEBSITE, path)
    return send_from_directory(WEBSITE, "index.html")


if __name__ == "__main__":
    print("DT lll live server: http://127.0.0.1:8000")
    app.run(host=os.getenv("DT_HOST", "127.0.0.1"), port=int(os.getenv("DT_PORT", "8000")), debug=False)
