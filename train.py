"""Train MIME-ID 300K on a curated simple-Indonesian corpus."""
import argparse
import random
from pathlib import Path
import torch
from model import BOS_ID, EOS_ID, ModelConfig, TinyLanguageModel

def load_documents(path):
    docs = [part.strip() for part in Path(path).read_text(encoding="utf-8").split("\n\n") if part.strip()]
    if len(docs) < 2:
        raise ValueError("Need at least two non-empty documents separated by blank lines.")
    return docs

def make_stream(documents):
    encoded = [torch.tensor([BOS_ID, *doc.encode("utf-8"), EOS_ID], dtype=torch.long) for doc in documents]
    return torch.cat(encoded)

def get_batch(stream, batch_size, block_size, device):
    if len(stream) < 2:
        raise ValueError("A data split must contain at least two tokens.")
    effective = min(block_size, len(stream) - 1)
    max_start = len(stream) - effective - 1
    starts = torch.randint(0, max_start + 1, (batch_size,))
    x = torch.stack([stream[s:s + effective] for s in starts])
    y = torch.stack([stream[s + 1:s + effective + 1] for s in starts])
    return x.to(device), y.to(device)

@torch.no_grad()
def estimate_loss(model, train_stream, val_stream, args, device):
    model.eval()
    result = {}
    for name, stream in (("train", train_stream), ("val", val_stream)):
        values = []
        for _ in range(args.eval_batches):
            x, y = get_batch(stream, args.batch_size, model.config.block_size, device)
            _, loss = model(x, y)
            values.append(loss.item())
        result[name] = sum(values) / len(values)
    model.train()
    return result

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", default="data/train.txt")
    parser.add_argument("--out-dir", default="checkpoints")
    parser.add_argument("--steps", type=int, default=6000)
    parser.add_argument("--batch-size", type=int, default=32)
    parser.add_argument("--learning-rate", type=float, default=3e-4)
    parser.add_argument("--eval-interval", type=int, default=500)
    parser.add_argument("--eval-batches", type=int, default=20)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--device", default="auto", choices=["auto", "cpu", "cuda", "mps"])
    args = parser.parse_args()
    random.seed(args.seed)
    torch.manual_seed(args.seed)
    if args.device == "auto":
        device = "cuda" if torch.cuda.is_available() else ("mps" if hasattr(torch.backends, "mps") and torch.backends.mps.is_available() else "cpu")
    else:
        device = args.device
    device = torch.device(device)
    docs = load_documents(args.data)
    random.shuffle(docs)
    split = max(1, int(0.9 * len(docs)))
    train_docs, val_docs = docs[:split], docs[split:]
    if not val_docs:
        raise ValueError("Need enough documents for validation.")
    train_stream, val_stream = make_stream(train_docs), make_stream(val_docs)
    config = ModelConfig()
    model = TinyLanguageModel(config).to(device)
    count = model.parameter_count()
    print(f"Device: {device}")
    print(f"Train documents: {len(train_docs)} | validation documents: {len(val_docs)}")
    print(f"Trainable parameters: {count:,}")
    if count != 298656:
        raise RuntimeError(f"Expected exactly 298,656 parameters, got {count:,}.")
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
            checkpoint = {"model": model.state_dict(), "config": model.config_dict(),
                "step": step, "train_loss": metrics["train"], "val_loss": metrics["val"],
                "parameter_count": count}
            torch.save(checkpoint, out_dir / "last.pt")
            if metrics["val"] < best_val:
                best_val = metrics["val"]
                torch.save(checkpoint, out_dir / "best.pt")
    print(f"Training complete. Best validation loss: {best_val:.4f}")

if __name__ == "__main__":
    main()
