"""Audit the current corpus filter without changing the training dataset."""
import json
import random
import re
from collections import Counter
from pathlib import Path
from datasets import load_dataset
from prepare_data import clean_text, extract_text, split_simple_chunks, is_simple_indonesian

STOPWORDS = set("""
yang dan di ke dari ini itu untuk dengan pada adalah bisa akan sudah belum tidak ada atau juga
karena kalau jika saat ketika dalam oleh sebagai lebih sangat kita kami mereka saya anda kamu dia
orang anak rumah hari waktu cara baik baru membuat melakukan menjadi memiliki dapat setiap banyak
sering masih hingga sampai seperti tentang namun tetapi maka sedang telah punya pergi datang makan minum
kecil besar satu dua siapa apa bagaimana mengapa kapan tempat nama hidup dunia keluarga teman
sekolah kerja belajar bermain jalan air makanan cerita
""".split())

def main():
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--dataset", default="vickyfatrian/vqfat-indo-corpus")
    p.add_argument("--config", default="cosmopedia_id")
    p.add_argument("--max-documents", type=int, default=50000)
    p.add_argument("--samples", type=int, default=80)
    args = p.parse_args()
    stream = load_dataset(args.dataset, args.config, split="train", streaming=True)
    accepted, seen = [], set()
    scanned = chunks_seen = 0
    for row in stream:
        scanned += 1
        raw = clean_text(extract_text(row))
        for chunk in split_simple_chunks(raw, 15, 90):
            chunks_seen += 1
            if not is_simple_indonesian(chunk, 15, 90):
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
        if scanned % 5000 == 0:
            print(f"scanned={scanned} accepted={len(accepted)}")
    if len(accepted) < 1000:
        raise RuntimeError(f"Audit only found {len(accepted)} chunks; expected >=1000")
    words = [re.findall(r"[A-Za-zÀ-ÿ]+", x.lower()) for x in accepted]
    all_words = [w for doc in words for w in doc]
    stop_coverage = [sum(w in STOPWORDS for w in doc) / max(1, len(doc)) for doc in words]
    lengths = [len(doc) for doc in words]
    counts = Counter(all_words)
    random.Random(20261124).shuffle(accepted)
    Path("audit").mkdir(exist_ok=True)
    Path("audit/current_corpus.txt").write_text("\n\n".join(accepted) + "\n", encoding="utf-8")
    samples = accepted[:args.samples]
    Path("audit/random_samples.txt").write_text("\n\n".join(samples) + "\n", encoding="utf-8")
    report = {
        "dataset": args.dataset, "config": args.config, "rows_scanned": scanned,
        "chunks_considered": chunks_seen, "unique_chunks_kept": len(accepted),
        "total_words": len(all_words), "unique_word_forms": len(counts),
        "mean_words_per_chunk": round(sum(lengths)/len(lengths), 2),
        "median_words_per_chunk": sorted(lengths)[len(lengths)//2],
        "mean_common_word_coverage": round(sum(stop_coverage)/len(stop_coverage), 4),
        "chunks_below_5pct_common_words": sum(x < .05 for x in stop_coverage),
        "chunks_below_10pct_common_words": sum(x < .10 for x in stop_coverage),
        "top_60_word_forms": counts.most_common(60),
        "samples_file": "random_samples.txt",
        "note": "Heuristic diagnostic only; common-word coverage is not a language-identification or grammar score."
    }
    Path("audit/report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    print("\n--- RANDOM SAMPLE ---")
    for i, sample in enumerate(samples[:20], 1):
        print(f"[{i}] {sample}")

if __name__ == "__main__":
    main()
