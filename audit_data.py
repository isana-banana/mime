"""Audit the everyday Indonesian corpus and save human-readable samples."""
import json
import random
import re
from collections import Counter
from pathlib import Path
from datasets import load_dataset
from prepare_data import clean_text, extract_text, split_simple_chunks, is_everyday_indonesian

def main():
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--dataset", default="uonlp/CulturaX")
    p.add_argument("--config", default="id")
    p.add_argument("--max-documents", type=int, default=50000)
    p.add_argument("--samples", type=int, default=100)
    args = p.parse_args()
    print(f"Auditing {args.dataset} / {args.config}")
    stream = load_dataset(args.dataset, args.config, split="train", streaming=True)
    accepted, seen = [], set()
    scanned = considered = 0
    for row in stream:
        scanned += 1
        raw = clean_text(extract_text(row))
        for chunk in split_simple_chunks(raw, 8, 55):
            considered += 1
            if not is_everyday_indonesian(chunk, 8, 55):
                continue
            key = chunk.lower()
            if key in seen:
                continue
            seen.add(key)
            accepted.append(chunk)
            if len(accepted) >= args.max_documents:
                break
        if len(accepted) >= args.max_documents:
            break
        if scanned % 10000 == 0:
            print(f"scanned={scanned:,} accepted={len(accepted):,}")
    if len(accepted) < 1000:
        raise RuntimeError(f"Only {len(accepted)} chunks from {scanned} pages; inspect source/config/filter.")
    words = [re.findall(r"[A-Za-zÀ-ÿ]+", x.lower()) for x in accepted]
    all_words = [w for doc in words for w in doc]
    counts = Counter(all_words)
    rng = random.Random(20261124)
    rng.shuffle(accepted)
    Path("audit").mkdir(exist_ok=True)
    Path("audit/current_corpus.txt").write_text("\n\n".join(accepted) + "\n", encoding="utf-8")
    samples = accepted[:args.samples]
    Path("audit/random_samples.txt").write_text("\n\n".join(samples) + "\n", encoding="utf-8")
    report = {
        "dataset": args.dataset, "config": args.config, "rows_scanned": scanned,
        "chunks_considered": considered, "unique_chunks_kept": len(accepted),
        "total_words": len(all_words), "unique_word_forms": len(counts),
        "mean_words_per_chunk": round(sum(map(len, words))/len(words), 2),
        "median_words_per_chunk": sorted(map(len, words))[len(words)//2],
        "top_60_word_forms": counts.most_common(60),
        "samples_file": "random_samples.txt",
        "note": "Automatic checks cannot judge naturalness. Review random_samples.txt before training."
    }
    Path("audit/report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    print("\n--- RANDOM SAMPLE ---")
    for i, sample in enumerate(samples[:30], 1):
        print(f"[{i}] {sample}")

if __name__ == "__main__":
    main()
