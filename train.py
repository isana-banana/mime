"""Train MIME-ID 100K on a UTF-8 Indonesian text corpus."""
import argparse
import random
from pathlib import Path

import torch

from model import BOS_ID, EOS_ID, ModelConfig, TinyLanguageModel


def load_documents(path):
    text = Path(path).read_text(encoding="utf-8")
    # Blank lines separate documents. Keep paragraph line breaks inside each document.
    docs = [part.strip() for part in text.split("\n\n") if part.strip()]
    if len(docs) < 2:
        raise ValueError("Need at least two non-empty documents separated by blank lines.")
    return docs


def encode_documents(documents):
    encoded = []
    for doc in documents:
        raw = list(doc.encode("utf-8"))
        encoded.append(torch.tensor([BOS_ID, *raw, EOS_ID], dtype=torch.long))
    return encoded


def make_stream(documents):
    return torch.cat(encode_documents(documents))


def get_batch(stream, batch_size, block_size, device):
    if len(stream) < 2:
        raise ValueError("A data split must contain at least two tokens. Add more documents.")
    # Short validation splits can use a shorter context; the model still accepts it.
    effective_block = min(block_size, len(stream) - 1)
    max_start = len(stream) - effective_block - 1
    starts = torch.randint(0, max_start + 1, (batch_size,))
    x = torch.stack([stream[s:s + effective_block] for s in starts])
    y = torch.stack([stream[s + 1:s + effective_block + 1] for s in starts])
    return x.to(device), y.to(device)


@torch.no_grad()
def estimate_loss(model, train_stream, val_stream, args, device):
    model.eval()
    results = {}
    for name, stream in (("train", train_stream), ("val", val_stream)):
        losses = []
        for _ in range(args.eval_batches):
            x, y = get_batch(stream, args.batch_size, model.config.block_size, device)
            _, loss = model(x, y)
            losses.append(loss.item())
        results[name] = sum(losses) / len(losses)
    model.train()
    return results


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", default="data/train.txt")
    parser.add_argument("--out-dir", default="checkpoints")
    parser.add_argument("--steps", type=int, default=10000)
    parser.add_argument("--batch-size", type=int, default=32)
    parser.add_argument("--learning-rate", type=float, default=3e-4)
    parser.add_argument("--eval-interval", type=int, default=500)
    parser.add_argument("--eval-batches", type=int, default=30)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--device", default="auto", choices=["auto", "cpu", "cuda", "mps"])
    args = parser.parse_args()

    random.seed(args.seed)
    torch.manual_seed(args.seed)
    if args.device == "auto":
        device = "cuda" if torch.cuda.is_available() else (
            "mps" if hasattr(torch.backends, "mps") and torch.backends.mps.is_available() else "cpu"
        )
    else:
        device = args.device
    device = torch.device(device)

    docs = load_documents(args.data)
    random.shuffle(docs)
    split = max(1, int(0.9 * len(docs)))
    train_docs, val_docs = docs[:split], docs[split:]
    if not val_docs:
        raise ValueError("Need enough documents for a validation split; add more documents.")

    train_stream, val_stream = make_stream(train_docs), make_stream(val_docs)
    config = ModelConfig()
    model = TinyLanguageModel(config).to(device)
    count = model.parameter_count()
    print(f"Device: {device}")
    print(f"Train documents: {len(train_docs)} | validation documents: {len(val_docs)}")
    print(f"Trainable parameters: {count:,}")
    if not 50_000 <= count <= 100_000:
        raise RuntimeError(f"Parameter count {count:,} is outside the required 50K–100K range.")

    optimizer = torch.optim.AdamW(model.parameters(), lr=args.learning_rate, weight_decay=0.01)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    best_val = float("inf")

    for step in range(1, args.steps + 1):
        model.train()
        x, y = get_batch(train_stream, args.batch_size, config.block_size, device)
        _, loss = model(x, y)
        optimizer.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        optimizer.step()

        if step == 1 or step % args.eval_interval == 0 or step == args.steps:
            metrics = estimate_loss(model, train_stream, val_stream, args, device)
            print(f"step {step:6d} | train {metrics['train']:.4f} | val {metrics['val']:.4f}")
            checkpoint = {
                "model": model.state_dict(),
                "config": model.config_dict(),
                "step": step,
                "train_loss": metrics["train"],
                "val_loss": metrics["val"],
                "parameter_count": count,
            }
            torch.save(checkpoint, out_dir / "last.pt")
            if metrics["val"] < best_val:
                best_val = metrics["val"]
                torch.save(checkpoint, out_dir / "best.pt")

    print(f"Training complete. Best validation loss: {best_val:.4f}")


if __name__ == "__main__":
    main()
