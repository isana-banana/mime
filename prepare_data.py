"""Fetch a bounded Indonesian corpus from Hugging Face at workflow runtime."""
import argparse
from pathlib import Path

from datasets import load_dataset


def extract_text(row):
    for key in ("text", "content", "document", "article", "body"):
        value = row.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    # Be resilient to a dataset schema change without silently emitting metadata.
    strings = [
        value.strip() for key, value in row.items()
        if key not in {"id", "url", "source", "metadata"}
        and isinstance(value, str) and len(value.strip()) > 80
    ]
    return max(strings, key=len) if strings else ""


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", default="vickyfatrian/vqfat-indo-corpus")
    parser.add_argument("--config", default="cosmopedia_id")
    parser.add_argument("--split", default="train")
    parser.add_argument("--max-documents", type=int, default=50000)
    parser.add_argument("--output", default="data/train.txt")
    args = parser.parse_args()

    print(f"Streaming {args.dataset} / {args.config} ({args.split})")
    stream = load_dataset(
        args.dataset, args.config, split=args.split, streaming=True
    )
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    count = 0
    total_chars = 0
    with output.open("w", encoding="utf-8") as handle:
        for row in stream:
            text = extract_text(row)
            if len(text) < 80:
                continue
            handle.write(text.replace("\x00", " ").strip() + "\n\n")
            count += 1
            total_chars += len(text)
            if count >= args.max_documents:
                break
    if count < 2:
        raise RuntimeError(
            "Dataset yielded fewer than two usable text documents; inspect its schema."
        )
    print(f"Wrote {count:,} documents ({total_chars:,} characters) to {output}")


if __name__ == "__main__":
    main()
