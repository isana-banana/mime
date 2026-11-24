"""Build a cleaner, everyday Indonesian corpus from natural web text.

The filter favors short, complete sentences and familiar words. It is deliberately
conservative about noisy pages, lists, machine-like text, and foreign-language
content. It cannot guarantee grammatical quality; audit samples before training.
"""
import argparse
import hashlib
import html
import re
import unicodedata
from pathlib import Path
from datasets import load_dataset

STOPWORDS = set("""
yang dan di ke dari ini itu untuk dengan pada adalah bisa akan sudah belum tidak ada atau juga
karena kalau jika saat ketika dalam oleh sebagai lebih sangat kita kami mereka saya anda kamu dia
orang anak rumah hari waktu cara baik baru membuat melakukan menjadi memiliki dapat setiap banyak
sering masih hingga sampai seperti tentang namun tetapi maka sedang telah punya pergi datang makan minum
kecil besar satu dua tiga siapa apa bagaimana mengapa kapan tempat nama hidup dunia keluarga teman
sekolah kerja belajar bermain jalan air makanan cerita bukan hanya semua sesuatu suatu ingin tahu jadi
saja lagi setelah sebelum selama tanpa antar antara terhadap melalui sekitar pertama kedua beberapa
cukup mungkin harus boleh perlu pernah selalu kadang hampir kembali mulai gunakan memakai tinggal
""".split())

COMMON_WORDS = STOPWORDS | set("""
aku enggak nggak gak kok sih dong deh yuk ayo nih tuh banget bangetnya
pagi siang sore malam rumah kamar dapur pintu meja kursi motor mobil bus pasar warung toko
ayah ibu bapak mama kakak adik teman tetangga guru murid anak-anak
makan nasi sayur buah telur ikan ayam roti kopi teh air tidur bangun mandi masak cuci
pergi pulang datang jalan duduk berdiri lihat dengar bicara cerita tanya jawab bilang
senang sedih takut capek lapar haus suka mau cari ambil kasih bantu coba tunggu
sekarang besok kemarin tadi nanti hari minggu senin selasa rabu kamis jumat sabtu
""".split())

ENGLISH_MARKERS = set("""
the and is are was were be been being of to for from with without this that these those
you your we our they their he she his her as at by on in into about can could would should
will do does did have has had if then than but or so because when where what who why how
""".split())

BAD_PHRASES = (
    "pada suatu ketika", "di sebuah negeri yang jauh", "dahulu kala",
    "tidak dapat mempercayai matanya", "permata tersembunyi", "dalam cerita kita",
    "seperti yang telah disebutkan", "dapat disimpulkan bahwa",
    "oleh karena itu dapat", "secara komprehensif", "paradigma",
    "mengimplementasikan", "mengoptimalisasi", "mengejawantahkan",
)
BAD_LABEL = re.compile(
    r"(^|\\s)(alice|bob|assistant|user|system|mommy|daddy|mr\\.?|mrs\\.?|ms\\.?|miss)\\s*:",
    re.IGNORECASE,
)
WORD_RE = re.compile(r"[A-Za-zÀ-ÿ]+")

def extract_text(row):
    for key in ("text", "content", "document", "article", "body"):
        value = row.get(key)
        if isinstance(value, str) and value.strip():
            return value
    return ""

def clean_text(value):
    value = html.unescape(value)
    value = re.sub(r"<[^>]+>", " ", value)
    value = re.sub(r"https?://\\S+|www\\.\\S+", " ", value)
    value = re.sub(r"(?m)^\\s{0,3}#{1,6}\\s*", "", value)
    value = re.sub(r"[\\x00-\\x08\\x0b\\x0c\\x0e-\\x1f]", " ", value)
    value = unicodedata.normalize("NFKC", value)
    value = re.sub(r"[ \\t]+", " ", value)
    value = re.sub(r"\\n{3,}", "\\n\\n", value)
    return value.strip()

def split_simple_chunks(text, min_words=8, max_words=55):
    sentences = re.split(r"(?<=[.!?])\\s+|\\n+", text)
    chunks, current, count = [], [], 0
    for sentence in sentences:
        sentence = sentence.strip(" -•*\\t")
        words = WORD_RE.findall(sentence)
        if not min_words <= len(words) <= 32:
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

def is_everyday_indonesian(text, min_words=8, max_words=55):
    words = WORD_RE.findall(text.lower())
    n = len(words)
    if not min_words <= n <= max_words:
        return False
    lower = text.lower()
    if BAD_LABEL.search(text) or any(p in lower for p in BAD_PHRASES):
        return False
    if sum(len(w) >= 13 for w in words) / n > 0.08:
        return False
    if sum(ch.isdigit() for ch in text) / max(1, len(text)) > 0.04:
        return False
    if sum(not ch.isalnum() and not ch.isspace() for ch in text) / max(1, len(text)) > 0.09:
        return False
    if sum(w in ENGLISH_MARKERS for w in words) / n > 0.015:
        return False
    common = sum(w in COMMON_WORDS for w in words)
    if common < 4 or common / n < 0.16:
        return False
    if len({w for w in words if w in COMMON_WORDS}) < 4:
        return False
    # Reject headlines, fragments, and text that looks like a navigation menu.
    if not re.search(r"[.!?](?:\\s|$)", text):
        return False
    if text.count("|") or text.count("•") > 1:
        return False
    # Very long capitalized runs often come from names, titles, or scraped menus.
    caps = re.findall(r"\\b[A-Z][a-zÀ-ÿ]{2,}\\b", text)
    if sum(text.find(w) > 0 for w in caps) > max(3, n // 12):
        return False
    return True

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--dataset", default="uonlp/CulturaX")
    p.add_argument("--config", default="id")
    p.add_argument("--split", default="train")
    p.add_argument("--max-documents", type=int, default=50000)
    p.add_argument("--min-words", type=int, default=8)
    p.add_argument("--max-words", type=int, default=55)
    p.add_argument("--output", default="data/train.txt")
    args = p.parse_args()

    print(f"Streaming natural Indonesian web text: {args.dataset} / {args.config}")
    stream = load_dataset(args.dataset, args.config, split=args.split, streaming=True)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    seen, count, total_words, scanned = set(), 0, 0, 0
    with output.open("w", encoding="utf-8") as handle:
        for row in stream:
            scanned += 1
            raw = clean_text(extract_text(row))
            for chunk in split_simple_chunks(raw, args.min_words, args.max_words):
                if not is_everyday_indonesian(chunk, args.min_words, args.max_words):
                    continue
                digest = hashlib.sha1(chunk.lower().encode("utf-8")).hexdigest()
                if digest in seen:
                    continue
                seen.add(digest)
                handle.write(chunk + "\\n\\n")
                count += 1
                total_words += len(WORD_RE.findall(chunk))
                if count >= args.max_documents:
                    break
            if count >= args.max_documents:
                break
            if scanned % 10000 == 0:
                print(f"Scanned {scanned:,} pages; kept {count:,} chunks")
    if count < 1000:
        raise RuntimeError(
            f"Only {count} usable chunks from {scanned} pages. "
            "Check dataset access/config or review the filter."
        )
    print(f"Saved {count:,} unique everyday Indonesian chunks ({total_words:,} words) "
          f"from {scanned:,} pages to {output}")

if __name__ == "__main__":
    main()
