# MIME-ID 100K

Tiny Indonesian byte-level decoder-only Transformer. This is a learning/research prototype, not a capable modern assistant.

## Model

- Indonesian-only training corpus
- 256 UTF-8 byte tokens + BOS + EOS = vocabulary 258
- Context length: 128
- Embedding width: 64
- Transformer layers: 2
- Attention heads: 4
- Feed-forward width: 128
- Tied token embedding and output weights
- **91,776 trainable parameters** with the default configuration

`train.py` checks the parameter count and refuses to train if it is outside 50,000–100,000.

## Setup

```bash
python -m venv .venv
# Linux/macOS:
source .venv/bin/activate
# Windows:
# .venv\Scripts\activate
pip install -r requirements.txt
```

Put a UTF-8 Indonesian corpus at `data/train.txt`. Separate documents with blank lines. See `data/README.md`.

## Train

```bash
python train.py --data data/train.txt --steps 10000
```

Useful options: `--batch-size`, `--learning-rate`, `--eval-interval`, and `--device cpu|cuda|mps|auto`.

## Generate

```bash
python generate.py --checkpoint checkpoints/best.pt --prompt "Bahasa Indonesia adalah"
```

## Important limitations

91K parameters is extremely small. Expect short, repetitive, error-prone text; it will not have the reasoning, factual recall, or instruction-following ability of a modern LLM. Byte-level tokenization handles Indonesian UTF-8 correctly but consumes more context positions than subword tokenization. Training quality depends heavily on corpus quality and size.
