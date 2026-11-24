"""Prepare cleaner, simple Indonesian text from the HF corpus.

This remains a heuristic filter: it reduces obvious English contamination,
synthetic dialogue labels, and story-translation artifacts, but cannot certify
that every retained sentence is idiomatic Indonesian.
"""
import argparse
import hashlib
import html
import re
import unicodedata
from pathlib import Path
from datasets import load_dataset

STOPWORDS_ID = set("""
yang dan di ke dari ini itu untuk dengan pada adalah bisa akan sudah belum tidak ada atau juga
karena kalau jika saat ketika dalam oleh sebagai lebih sangat kita kami mereka saya anda kamu dia
orang anak rumah hari waktu cara baik baru membuat melakukan menjadi memiliki dapat setiap banyak
sering masih hingga sampai seperti tentang namun tetapi maka sedang telah punya pergi datang makan minum
kecil besar satu dua tiga siapa apa bagaimana mengapa kapan tempat nama hidup dunia keluarga teman
sekolah kerja belajar bermain jalan air makanan cerita bukan hanya semua sesuatu suatu ingin tahu jadi
saja lagi masih setelah sebelum selama tanpa antar antara terhadap melalui sekitar pertama kedua beberapa
cukup mungkin harus boleh perlu sedang pernah selalu kadang hampir kembali mulai gunakan memakai tinggal
berada terlihat merasa berkata tanya jawab pikir kasih beri ambil cari pakai bantu tahu punya milik
""".split())

COMMON_ID = STOPWORDS_ID | set("""
merupakan terdapat bagian bentuk contoh jenis hasil penggunaan dikenal disebut manusia alam benda
tubuh mata kepala tangan kaki makan minuman keluarga teman anak perempuan laki laki ibu ayah pagi
siang sore malam rumah sekolah pasar toko jalan kota desa negara dunia hidup pekerjaan uang harga
barang warna ukuran besar kecil panjang pendek tinggi rendah cepat lambat mudah sulit penting benar
salah baik buruk baru lama dekat jauh banyak sedikit semua setiap beberapa sendiri bersama orang-orang
""".split())

ENGLISH_MARKERS = set("""
the and is are was were be been being of to for from with without this that these those it its
you your we our they their he she his her as at by on in into about can could would should will
not do does did have has had if then than but or so because when where what who why how which
""".split())

TRANSLATION_ARTIFACTS = (
    "pada suatu ketika", "di sebuah negeri yang jauh", "dahulu kala",
    "merasa penasaran", "mengangguk dan menjawab", "tersenyum dan berkata",
    "berseru", "menghujani", "kupu-kupu tersebut", "dengan lembut",
    "tidak dapat mempercayai matanya", "seperti permainan yang",
    "dalam cerita kita", "sekarang, saya tahu", "permata tersembunyi",
    "bukan hanya", "faktanya,", "lagipula,", "kerja bagus dengan",
)

DIALOGUE_LABEL = re.compile(
    r"(^|\s)(alice|bob|mommy|daddy|mr\.?|mrs\.?|ms\.?|miss)\s*:",
    re.IGNORECASE,
)
WORD_RE = re.compile(r"[A-Za-zÀ-ÿ]+")

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
        words = WORD_RE.findall(sentence)
        if len(words) < 5 or len(words) > 38:
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
    words = WORD_RE.findall(text.lower())
    n = len(words)
    if not min_words <= n <= max_words:
        return False
    if sum(len(w) >= 13 for w in words) / n > 0.12:
        return False
    if sum(ch.isdigit() for ch in text) / max(1, len(text)) > 0.08:
        return False
    if sum(not ch.isalnum() and not ch.isspace() for ch in text) / max(1, len(text)) > 0.12:
        return False
    if DIALOGUE_LABEL.search(text):
        return False
    lower = text.lower()
    if any(phrase in lower for phrase in TRANSLATION_ARTIFACTS):
        return False
    stop_count = sum(w in STOPWORDS_ID for w in words)
    if stop_count < 5 or stop_count / n < 0.12:
        return False
    if len({w for w in words if w in STOPWORDS_ID}) < 4:
        return False
    if sum(w in ENGLISH_MARKERS for w in words) / n > 0.025:
        return False
    if sum(w in COMMON_ID for w in words) < 7:
        return False
    # Reject chunks dominated by named entities / title-cased names.
    tokens = re.findall(r"\b[A-Z][a-zÀ-ÿ]{2,}\b", text)
    internal_caps = sum(1 for token in tokens if text.find(token) > 0)
    if internal_caps > max(2, n // 18):
        return False
    # Prefer complete, readable sentences over fragments.
    if len(re.findall(r"[.!?](?:\s|$)", text)) == 0:
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
                total_words += len(WORD_RE.findall(chunk))
                if count >= args.max_documents:
                    break
            if count >= args.max_documents:
                break
            if scanned % 5000 == 0:
                print(f"Scanned {scanned:,} rows; kept {count:,} chunks")
    if count < 1000:
        raise RuntimeError(f"Only {count} usable chunks from {scanned} rows. "
            "The source may not contain enough natural Indonesian text.")
    print(f"Saved {count:,} unique filtered Indonesian chunks ({total_words:,} words) "
        f"from {scanned:,} rows to {output}")

if __name__ == "__main__":
    main()
