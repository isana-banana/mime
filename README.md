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


## Train on GitHub Actions

1. Add your permitted UTF-8 Indonesian corpus as `data/train.txt` (blank lines separate documents). Keep private or sensitive text out of the corpus.
2. Open the repository's **Actions** tab.
3. Select **Train MIME-ID 100K**, choose **Run workflow**, set the step count and batch size, then start it.
4. When the run finishes, download the `mime-id-100k-checkpoints` artifact from that workflow run. It contains `best.pt` and `last.pt`.

The workflow uses a GitHub-hosted CPU runner. Runtime depends on corpus size and step count; GitHub Actions usage limits and billing may apply. The workflow does not start automatically and will fail until `data/train.txt` is present.


## Fully automated corpus preparation

The GitHub Actions workflow can fetch a bounded Indonesian pretraining corpus directly from Hugging Face at runtime; no manual `data/train.txt` upload is required. It currently streams up to 50,000 documents from the `cosmopedia_id` configuration of [VQFat Indonesian Corpus](https://huggingface.co/datasets/vickyfatrian/vqfat-indo-corpus), then runs 10,000 CPU training steps by default.

Dataset attribution: Vicky Fatrian, *VQFat Indonesian Corpus* (2026). Its C-UDA terms permit AI/ML training and require attribution; see the dataset card and license before reusing or redistributing corpus material. This workflow uses the pretraining subset only, not the separate Aurora instruction subset.

The workflow is configured for manual dispatch and automatic runs when its workflow, data-preparation script, or requirements change on `main`. Check the Actions tab for run status and download the `mime-id-100k-checkpoints` artifact after a successful run. GitHub-hosted runners are CPU-only here, and GitHub Actions quotas/billing may apply.
