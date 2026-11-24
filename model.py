"""MIME-ID 300K: compact byte-level Indonesian decoder-only Transformer."""
from dataclasses import asdict, dataclass
import torch
import torch.nn as nn
import torch.nn.functional as F

BOS_ID = 256
EOS_ID = 257

@dataclass
class ModelConfig:
    vocab_size: int = 258
    block_size: int = 128
    n_embd: int = 96
    n_layer: int = 3
    n_head: int = 4
    n_ff: int = 256
    dropout: float = 0.1

class CausalSelfAttention(nn.Module):
    def __init__(self, config):
        super().__init__()
        assert config.n_embd % config.n_head == 0
        self.n_head = config.n_head
        self.head_dim = config.n_embd // config.n_head
        self.qkv = nn.Linear(config.n_embd, 3 * config.n_embd)
        self.proj = nn.Linear(config.n_embd, config.n_embd)
        self.dropout = config.dropout

    def forward(self, x):
        batch, length, channels = x.shape
        q, k, v = self.qkv(x).split(channels, dim=-1)
        def split_heads(t):
            return t.view(batch, length, self.n_head, self.head_dim).transpose(1, 2)
        q, k, v = split_heads(q), split_heads(k), split_heads(v)
        y = F.scaled_dot_product_attention(q, k, v, attn_mask=None,
            dropout_p=self.dropout if self.training else 0.0, is_causal=True)
        y = y.transpose(1, 2).contiguous().view(batch, length, channels)
        return self.proj(y)

class MLP(nn.Module):
    def __init__(self, config):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(config.n_embd, config.n_ff), nn.GELU(),
            nn.Linear(config.n_ff, config.n_embd), nn.Dropout(config.dropout))

    def forward(self, x):
        return self.net(x)

class TransformerBlock(nn.Module):
    def __init__(self, config):
        super().__init__()
        self.ln1 = nn.LayerNorm(config.n_embd)
        self.attn = CausalSelfAttention(config)
        self.ln2 = nn.LayerNorm(config.n_embd)
        self.mlp = MLP(config)

    def forward(self, x):
        x = x + self.attn(self.ln1(x))
        return x + self.mlp(self.ln2(x))

class TinyLanguageModel(nn.Module):
    def __init__(self, config=None):
        super().__init__()
        self.config = config or ModelConfig()
        c = self.config
        self.token_embedding = nn.Embedding(c.vocab_size, c.n_embd)
        self.position_embedding = nn.Embedding(c.block_size, c.n_embd)
        self.drop = nn.Dropout(c.dropout)
        self.blocks = nn.Sequential(*[TransformerBlock(c) for _ in range(c.n_layer)])
        self.final_norm = nn.LayerNorm(c.n_embd)
        self.lm_head = nn.Linear(c.n_embd, c.vocab_size, bias=False)
        self.lm_head.weight = self.token_embedding.weight
        self.apply(self._init_weights)

    @staticmethod
    def _init_weights(module):
        if isinstance(module, nn.Linear):
            nn.init.normal_(module.weight, mean=0.0, std=0.02)
            if module.bias is not None:
                nn.init.zeros_(module.bias)
        elif isinstance(module, nn.Embedding):
            nn.init.normal_(module.weight, mean=0.0, std=0.02)

    def forward(self, idx, targets=None):
        _, length = idx.shape
        if length > self.config.block_size:
            raise ValueError(f"Sequence length {length} exceeds block_size={self.config.block_size}")
        positions = torch.arange(length, device=idx.device)
        x = self.drop(self.token_embedding(idx) + self.position_embedding(positions))
        logits = self.lm_head(self.final_norm(self.blocks(x)))
        loss = None
        if targets is not None:
            loss = F.cross_entropy(logits.reshape(-1, logits.size(-1)), targets.reshape(-1))
        return logits, loss

    def parameter_count(self):
        return sum(p.numel() for p in self.parameters() if p.requires_grad)

    def config_dict(self):
        return asdict(self.config)
