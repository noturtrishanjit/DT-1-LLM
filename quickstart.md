# DT lll

DT lll is a small, CPU-first language-model starter kit for conversation, student-level math, and simple Java. It is intentionally a learning project, not a claim of frontier-model capability.

## Architecture

The default configuration is a decoder-only causal Transformer with **4 blocks**, **256 hidden dimensions**, **8 attention heads**, **1,024-dimensional feed-forward layers**, **512-token context**, and a **259-token byte vocabulary** with tied embeddings. That is approximately **3.7M parameters**, inside the requested 1–5M range. The included byte-level tokenizer is deterministic and dependency-free; for a serious run, replace it with a trained BPE/SentencePiece tokenizer and keep the vocabulary near 4k if you later replace the byte tokenizer.

## Quickstart

```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
source .venv/bin/activate
pip install -r model/requirements.txt
python model/train.py --data data/train.jsonl --steps 100 --device cpu
python model/infer.py --checkpoint checkpoints/best.pt --prompt "Solve 2x + 6 = 14 step by step."
python model/evaluate.py --checkpoint checkpoints/best.pt --data data/eval.jsonl
```

Training records are JSONL objects with `prompt`, `response`, and optional `kind` fields. Put your licensed data under `data/`; the repository intentionally does not bundle scraped or restricted corpora. The training script also accepts plain text files with one prompt-response pair per line only if you adapt `load_records`.

## Data plan

Start with a small, high-quality instruction mixture: friendly conversational examples; synthetic arithmetic and grade-school algebra with explicit working; and hand-reviewed beginner Java examples covering variables, conditions, loops, arrays, methods, and debugging. GSM8K-style data is useful as a format reference, but check its license and do not assume that a benchmark license covers redistribution. For conversations, use permissively licensed instruction data or your own authored examples. Keep a 10–20% replay slice of conversation in later math/Java stages so the model does not forget its tone.

A practical schedule is: tokenizer/data validation; 1–3 epochs of mixed pretraining or continued training; supervised instruction tuning with short sequences; then a final low learning-rate pass on balanced, held-out examples. Use packed sequences, gradient accumulation, and early stopping. On a modern CPU, smoke tests are easy but meaningful training may take days. A small 8–16GB GPU is much more practical. The model itself should use well under 1GB RAM at inference; actual usage depends on PyTorch overhead and sequence length.

## Quantization

`infer.py --quantize int8` applies PyTorch dynamic INT8 quantization to linear layers on CPU. It is the simplest portable option. A custom 4-bit export is not included because generic GGUF conversion expects a compatible architecture; for 4-bit deployment, either add a custom converter/kernel or port the learned weights into a supported llama.cpp-compatible architecture while preserving the tokenizer and prompt format.

## Evaluation

Run separate tests for chat style, exact math answers, and Java correctness. `evaluate.py` reports simple exact/substring checks and writes generations for human review. For Java, compile generated snippets with `javac` in a sandbox and run unit-style cases. For math, compare normalized final answers and manually sample reasoning. Track failure categories rather than one blended score: tiny models can be pleasant conversationally while still being weak at multi-step reasoning.

## Limits

At 3.7M parameters, DT lll will have a very small factual memory, weak long-context behavior, and a high risk of arithmetic or code hallucinations. It should not be used for medical, legal, financial, security-critical, or production-code decisions. Prompt formatting, clean examples, constrained task scope, and verification matter more here than adding a few noisy gigabytes of data.

See [`docs/system_prompt.md`](docs/system_prompt.md) for the master prompt and [`website/index.html`](website/index.html) for the local product site.
