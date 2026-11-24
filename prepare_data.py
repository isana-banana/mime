"""Prepare short, readable Indonesian chunks from the existing HF corpus."""
import argparse
import hashlib
import html
import re
import unicodedata
from pathlib import Path
from datasets import load_dataset

COMMON_ID = set("""
yang dan di ke dari ini itu untuk dengan pada adalah bisa akan sudah belum tidak ada atau juga
karena kalau jika saat ketika dalam oleh sebagai lebih sangat kita kami mereka saya anda kamu dia
orang anak rumah hari waktu cara baik baru membuat melakukan menjadi memiliki dapat setiap banyak
sering masih hingga sampai seperti tentang namun tetapi maka sedang telah punya pergi datang makan minum
kecil besar satu dua tiga siapa apa bagaimana mengapa kapan tempat nama hidup dunia keluarga teman
sekolah kerja belajar bermain jalan air makanan cerita
""".split())

def extract_text(row):
    for key in ("text", "content", "document", "article", "body"):
        value = row.get(key)
        if isinstance(value, str) and value.strip():
            return value
    candidates = [v for k, v in row.items()
        if k not in {"id", "url", "source", "metadata"}
        and isinstance(v, str) and len(v.strip()) > 80]
    return max(candidates, key=len) if candidates else ""

def clean_text(value):
    value = html.unescape(value)
    value = re.sub(r"<[^>]+>", " ", value)
    value = re.sub(r"https?://\S+|www\.\S+", " ", value)
    value = re.sub(r"^\s{0,3}#{1,6}\s*", "", value, flags=re.MULTILINE)
    value = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", " ", value)
    value = unicodedata.normalize("NFKC", value)
    value = re.sub(r"[ \t]+", " ", value)
    value = re.sub(r"\n{3,}", "\n\n", value)
    return value.strip()

def split_simple_chunks(text, min_words, max_words):
    sentences = re.split(r"(?<=[.!?])\s+|\n+", text)
    chunks, current, count = [], [], 0
    for sentence in sentences:
        sentence = sentence.strip(" -•\t")
        words = re.findall(r"[A-Za-zÀ-ÿ]+", sentence)
        if len(words) < 4 or len(words) > 45:
            continue
        if count and count + len(words) > max_words:
            if count >= min_words:
                chunks.append(" ".join(current))
            current, count = [], 0
        current.append(sentence)
        count += len(words)
    if count >= min_words:
        chunks.append(" ".join(current))
    return chunks

def is_simple_indonesian(text, min_words, max_words):
    words = re.findall(r"[A-Za-zÀ-ÿ]+", text.lower())
    if not min_words <= len(words) <= max_words:
        return False
    if sum(len(w) >= 13 for w in words) / len(words) > 0.18:
        return False
    if sum(w in COMMON_ID for w in words) < 2:
        return False
    if sum(ch.isdigit() for ch in text) / max(1, len(text)) > 0.12:
        return False
    if sum(not ch.isalnum() and not ch.isspace() for ch in text) / max(1, len(text)) > 0.18:
        return False
    return True

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", default="vickyfatrian/vqfat-indo-corpus")
    parser.add_argument("--config", default="cosmopedia_id")
    parser.add_argument("--split", default="train")
    parser.add_argument("--max-documents", type=int, default=50000)
    parser.add_argument("--min-words", type=int, default=15)
    parser.add_argument("--max-words", type=int, default=90)
    parser.add_argument("--output", default="data/train.txt")
    args = parser.parse_args()
    print(f"Streaming {args.dataset} / {args.config} ({args.split})")
    stream = load_dataset(args.dataset, args.config, split=args.split, streaming=True)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    seen, count, total_words, scanned = set(), 0, 0, 0
    with output.open("w", encoding="utf-8") as handle:
        for row in stream:
            scanned += 1
            raw = clean_text(extract_text(row))
            for chunk in split_simple_chunks(raw, args.min_words, args.max_words):
                if not is_simple_indonesian(chunk, args.min_words, args.max_words):
                    continue
                digest = hashlib.sha1(chunk.lower().encode("utf-8")).hexdigest()
                if digest in seen:
                    continue
                seen.add(digest)
                handle.write(chunk + "\n\n")
                count += 1
                total_words += len(chunk.split())
                if count >= args.max_documents:
                    break
            if count >= args.max_documents:
                break
            if scanned % 5000 == 0:
                print(f"Scanned {scanned:,} rows; kept {count:,} chunks")
    if count < 1000:
        raise RuntimeError(f"Only {count} usable chunks from {scanned} rows. "
            "Check source schema or relax filters.")
    print(f"Saved {count:,} unique simple Indonesian chunks ({total_words:,} words) "
        f"from {scanned:,} rows to {output}")

if __name__ == "__main__":
    main()
