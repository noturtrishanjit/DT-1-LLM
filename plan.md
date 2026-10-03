# DT lll — implementation plan

## Product
A tiny, CPU-first language model starter kit and its documentation website. DT lll is designed around constrained inference rather than pretending to match large assistants.

## Model decisions
- Decoder-only causal Transformer, 4 blocks, hidden size 256, 8 attention heads, FFN size 1024, context length 512.
- Parameter count is approximately 3.7M with a 259-token byte vocabulary and tied input/output embeddings. This fits the requested 1–5M band.
- Byte-level BPE is recommended for production; the runnable starter uses a deterministic byte tokenizer so the repo works without external tokenizer files. A SentencePiece/BPE tokenizer can be swapped in later.
- Training is staged: conversational instruction data first, then math and Java examples, with a small high-quality replay mix to reduce catastrophic forgetting.
- Runtime is PyTorch CPU-only with optional dynamic INT8 linear quantization. True 4-bit export is documented as a future llama.cpp/GGUF path because this custom architecture is not directly compatible with a stock Llama converter.

## Website design
- Design movement: dark developer-tool landing page with editorial technical documentation.
- Core principles: high contrast, sparse surfaces, purposeful monospace accents, visible constraints.
- Color philosophy: near-black graphite for focus, warm paper text for readability, electric mint as the ownable signal color, and amber for caveats.
- Layout paradigm: asymmetric split hero, stacked horizontal spec bands, and a docs rail rather than a conventional centered marketing grid.
- Signature elements: mint “signal” cursor, parameter telemetry cards, and tiny status chips.
- Interaction: demo chat is explicitly labeled simulated and prioritizes honest feedback over fake inference.
- Animation: short, reduced-motion-friendly fades and a slow signal pulse; no decorative motion in the core reading path.
- Typography: Inter/system sans for UI and IBM Plex Mono-style fallbacks for code and telemetry.
- Brand essence: a tiny, honest AI lab for low-end machines. Personality: practical, curious, unpretentious.
- Voice: “Small enough to understand.” / “Bring the potato PC.”
- Wordmark: split “DT” block plus lowercase “lll” signal bars.
- Signature color: electric mint `#b8f56b`.

## Project structure
- `website/`: zero-dependency responsive site (`index.html`, `styles.css`, `app.js`, `manus-routes.json`).
- `model/`: PyTorch config, tokenizer, dataset utilities, training script, inference script, evaluation script, and requirements.
- `docs/`: system prompt and model README with commands, data guidance, limits, and evaluation notes.

## Delivery assumptions
- The demo is simulated in-browser and clearly marked; no backend or hosted model endpoint is assumed.
- Training data is user-supplied or downloaded from datasets whose licenses permit the intended use. The code accepts JSONL records and does not bundle third-party data.
- Commands target Python 3.10+ and PyTorch 2.x. CPU training for a 3.7M model is feasible for experiments but will be slow; a small GPU is recommended for serious pretraining.
