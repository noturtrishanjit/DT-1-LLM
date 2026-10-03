"""DT lll: a small decoder-only Transformer and dependency-free byte tokenizer."""
from dataclasses import asdict, dataclass
from typing import Dict, List
import torch
from torch import nn

class ByteTokenizer:
    """Maps UTF-8 bytes to stable IDs; no vocabulary file is required."""
    BOS, EOS, PAD = 256, 257, 258
    vocab_size = 259
    def encode(self, text: str, add_bos=True, add_eos=True) -> List[int]:
        ids = ([self.BOS] if add_bos else []) + list(text.encode("utf-8"))
        return ids + ([self.EOS] if add_eos else [])
    def decode(self, ids: List[int]) -> str:
        raw = bytes(i for i in ids if 0 <= i < 256)
        return raw.decode("utf-8", errors="replace")

@dataclass
class ModelConfig:
    vocab_size: int = 259
    context_length: int = 512
    d_model: int = 256
    n_heads: int = 8
    n_layers: int = 4
    d_ff: int = 1024
    dropout: float = 0.0

class CausalSelfAttention(nn.Module):
    def __init__(self, cfg: ModelConfig):
        super().__init__()
        assert cfg.d_model % cfg.n_heads == 0
        self.n_heads = cfg.n_heads
        self.head_dim = cfg.d_model // cfg.n_heads
        self.qkv = nn.Linear(cfg.d_model, 3 * cfg.d_model, bias=False)
        self.proj = nn.Linear(cfg.d_model, cfg.d_model, bias=False)
        self.register_buffer("mask", torch.tril(torch.ones(cfg.context_length, cfg.context_length)).view(1, 1, cfg.context_length, cfg.context_length), persistent=False)
    def forward(self, x):
        b, t, c = x.shape
        q, k, v = self.qkv(x).split(c, dim=-1)
        shape = (b, t, self.n_heads, self.head_dim)
        q, k, v = [z.view(shape).transpose(1, 2) for z in (q, k, v)]
        scores = (q @ k.transpose(-2, -1)) / (self.head_dim ** 0.5)
        scores = scores.masked_fill(self.mask[:, :, :t, :t] == 0, torch.finfo(scores.dtype).min)
        weights = torch.softmax(scores, dim=-1)
        return self.proj((weights @ v).transpose(1, 2).contiguous().view(b, t, c))

class Block(nn.Module):
    def __init__(self, cfg):
        super().__init__()
        self.ln1 = nn.LayerNorm(cfg.d_model)
        self.attn = CausalSelfAttention(cfg)
        self.ln2 = nn.LayerNorm(cfg.d_model)
        self.mlp = nn.Sequential(nn.Linear(cfg.d_model, cfg.d_ff), nn.GELU(), nn.Linear(cfg.d_ff, cfg.d_model))
    def forward(self, x):
        x = x + self.attn(self.ln1(x))
        return x + self.mlp(self.ln2(x))

class TinyTransformer(nn.Module):
    def __init__(self, cfg: ModelConfig):
        super().__init__(); self.cfg = cfg
        self.tok_emb = nn.Embedding(cfg.vocab_size, cfg.d_model)
        self.pos_emb = nn.Embedding(cfg.context_length, cfg.d_model)
        self.blocks = nn.ModuleList([Block(cfg) for _ in range(cfg.n_layers)])
        self.ln_f = nn.LayerNorm(cfg.d_model)
        self.lm_head = nn.Linear(cfg.d_model, cfg.vocab_size, bias=False)
        self.lm_head.weight = self.tok_emb.weight
        self.apply(self._init)
    def _init(self, module):
        if isinstance(module, (nn.Linear, nn.Embedding)):
            nn.init.normal_(module.weight, mean=0.0, std=0.02)
            if isinstance(module, nn.Linear) and module.bias is not None: nn.init.zeros_(module.bias)
    def forward(self, idx, targets=None):
        b, t = idx.shape
        if t > self.cfg.context_length: raise ValueError(f"sequence length {t} exceeds context {self.cfg.context_length}")
        pos = torch.arange(t, device=idx.device)
        x = self.tok_emb(idx) + self.pos_emb(pos)[None, :, :]
        for block in self.blocks: x = block(x)
        logits = self.lm_head(self.ln_f(x))
        loss = None
        if targets is not None: loss = nn.functional.cross_entropy(logits.reshape(-1, logits.size(-1)), targets.reshape(-1), ignore_index=-100)
        return logits, loss
    @classmethod
    def from_checkpoint(cls, path, device="cpu"):
        ckpt = torch.load(path, map_location=device)
        cfg = ModelConfig(**ckpt["config"])
        model = cls(cfg).to(device); model.load_state_dict(ckpt["model"]); model.eval()
        return model, ByteTokenizer(), ckpt

def count_parameters(model: nn.Module) -> int:
    return sum(p.numel() for p in model.parameters())
