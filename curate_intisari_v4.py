#!/usr/bin/env python3
"""Conservative preparation of INTISARI V4 for MIME review.

This tool NEVER marks a conversation as training-ready. It preserves the raw
source, normalizes common pronouns, and separates obvious exclusions from
unreviewed candidates. Semantic quality still requires human review.\n# Pipeline revisions are validated by the dedicated curation workflow.
"""
from __future__ import annotations

import argparse
import collections
import hashlib
import json
import re
from pathlib import Path
from typing import Any

DIGITAL_TERMS = [
    "online shop", "online shopping", "toko online", "belanja online",
    "media sosial", "sosial media", "situs web", "platform digital",
    "e-commerce", "marketplace", "cashback", "kode promo", "internet",
    "aplikasi", "website", "email", "e-mail", "whatsapp", "instagram",
    "facebook", "twitter", "tiktok", "youtube", "ponsel", "smartphone",
    "gadget", "laptop", "komputer", "wifi", "wi-fi", "browser", "google",
    "streaming", "online", "chatbot", "hp", "handphone", "telepon", "tablet",
    "televisi", "tv", "game", "video game", "game online", "game mobile", "game pc",
    "main game", "pubg", "mobile legends", "iphone", "android", "samsung", "prosesor",
    "processor", "layar", "keyboard", "printer", "mouse", "kamera digital", "zalora",
    "shopee", "tokopedia", "bukalapak",
]
DIGITAL_RE = re.compile(
    r"\b(?:" + "|".join(re.escape(x) for x in sorted(DIGITAL_TERMS, key=len, reverse=True)) + r")\b",
    re.IGNORECASE,
)
BROKEN_WORDS = {
    "baikaa", "sedanggri", "keterpaskan", "mereko", "sarankin",
    "pertaya", "telfon", "kuliyah", "ngaburuhu", "dangdang",
    "dangdangan", "gesum", "ngapai", "martil", "pemeranakan",
}
BROKEN_RE = re.compile(r"\b(?:" + "|".join(map(re.escape, sorted(BROKEN_WORDS))) + r")\b", re.IGNORECASE)
REPEATED_WORD_RE = re.compile(r"\b(\w+)(?:\s+\1){1,}\b", re.IGNORECASE)
LONG_GIBBERISH_RE = re.compile(r"\b[A-Za-z]{19,}\b")
REPEATED_CHAR_RE = re.compile(r"(.)\1{3,}", re.IGNORECASE)
CASUAL_RE = re.compile(r"\b(gue|gua|gw|lo|lu|elo|elu|aku|kamu)\b", re.IGNORECASE)
SLANG_RE = re.compile(r"\b(gue|gua|gw|lo|lu|elo|elu)\b", re.IGNORECASE)
FORMAL_RE = re.compile(r"\b(saya|anda)\b", re.IGNORECASE)

def _replace_word(text: str, mapping: dict[str, str]) -> str:
    pattern = re.compile(r"\b(" + "|".join(map(re.escape, mapping)) + r")\b", re.IGNORECASE)
    def repl(match: re.Match[str]) -> str:
        old = match.group(0)
        new = mapping[old.lower()]
        return new.capitalize() if old[:1].isupper() else new
    return pattern.sub(repl, text)

def normalize_pronouns(messages: list[dict[str, Any]]) -> tuple[list[dict[str, str]], str]:
    """Normalize a whole dialogue consistently; do not mix aku-kamu with saya-Anda."""
    joined = " ".join(str(m.get("content", "")) for m in messages)
    slang_count = len(SLANG_RE.findall(joined))
    informal_count = len(re.findall(r"\b(aku|kamu)\b", joined, re.IGNORECASE))
    formal_count = len(FORMAL_RE.findall(joined))
    use_casual = slang_count > 0 or informal_count >= formal_count
    if use_casual:
        mapping = {
            "gue": "aku", "gua": "aku", "gw": "aku",
            "lo": "kamu", "lu": "kamu", "elo": "kamu", "elu": "kamu",
            "saya": "aku", "anda": "kamu",
        }
        register = "aku-kamu"
    else:
        mapping = {
            "gue": "saya", "gua": "saya", "gw": "saya",
            "lo": "Anda", "lu": "Anda", "elo": "Anda", "elu": "Anda",
            "aku": "saya", "kamu": "Anda",
        }
        register = "saya-Anda"
    normalized = []
    for m in messages:
        content = _replace_word(str(m.get("content", "")).strip(), mapping)
        normalized.append({"role": str(m.get("role", "")), "content": content})
    return normalized, register

def inspect_conversation(item: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    messages = item.get("messages")
    if not isinstance(messages, list) or len(messages) < 2:
        return ["struktur_giliran"]
    roles = [m.get("role") if isinstance(m, dict) else None for m in messages]
    if roles[0] != "user" or roles[-1] != "assistant" or any(
        roles[i] == roles[i - 1] for i in range(1, len(roles))
    ) or any(role not in ("user", "assistant") for role in roles):
        reasons.append("struktur_giliran")
    contents = []
    for m in messages:
        content = m.get("content", "") if isinstance(m, dict) else ""
        if not isinstance(content, str) or not content.strip():
            reasons.append("pesan_kosong")
            content = ""
        contents.append(content.strip())
    joined = " ".join(contents)
    if DIGITAL_RE.search(joined):
        reasons.append("topik_digital")
    if BROKEN_RE.search(joined):
        reasons.append("kata_rusak_dikenali")
    if REPEATED_WORD_RE.search(joined):
        reasons.append("pengulangan_kata")
    if REPEATED_CHAR_RE.search(joined) or LONG_GIBBERISH_RE.search(joined):
        reasons.append("pola_teks_mencurigakan")
    if len(messages) > 12:
        reasons.append("terlalu_panjang")
    if len(joined) > 2400:
        reasons.append("teks_terlalu_panjang")
    # Very short replies are usually not useful as supervised chat examples.
    if any(len(c.split()) < 2 for c in contents):
        reasons.append("pesan_terlalu_pendek")
    # A reply that mostly copies the immediately preceding user message is weak.
    if len(messages) >= 2:
        u = contents[-2].lower()
        a = contents[-1].lower()
        uw = set(re.findall(r"\b\w+\b", u))
        aw = set(re.findall(r"\b\w+\b", a))
        if len(uw) >= 5 and len(uw & aw) / max(1, len(uw)) >= 0.78:
            reasons.append("jawaban_mengulang_pengguna")
    if SPEAKER_LABEL_RE.search(joined):
        reasons.append("label_pembicara_di_dalam_teks")
    # Register mixing is not necessarily fatal; mark for review after normalization.
    if SLANG_RE.search(joined) and FORMAL_RE.search(joined):
        reasons.append("campuran_register_awal")
    # Simple anomaly patterns observed during source inspection.
    if re.search(r"\b(?:mau ngapain apa|yang ngapain sama|apa yang .* apa|(?:aku|saya|kamu|anda) siapa)\b", joined, re.IGNORECASE):
        reasons.append("susunan_kalimat_janggal")
    return sorted(set(reasons))

def process(input_path: Path, output_dir: Path, limit: int | None = None) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    candidates_path = output_dir / "candidate_unreviewed.jsonl"
    quarantine_path = output_dir / "quarantine.jsonl"
    review_path = output_dir / "manual_review_sample.jsonl"
    reason_counts: collections.Counter[str] = collections.Counter()
    role_counts: collections.Counter[str] = collections.Counter()
    length_counts: collections.Counter[str] = collections.Counter()
    total = malformed = candidate_count = quarantined = 0
    review_samples: list[dict[str, Any]] = []
    seen_hashes: set[str] = set()

    with input_path.open(encoding="utf-8") as src, \
         candidates_path.open("w", encoding="utf-8") as cand, \
         quarantine_path.open("w", encoding="utf-8") as quarantine:
        for line_no, line in enumerate(src, 1):
            if limit is not None and total >= limit:
                break
            try:
                item = json.loads(line)
            except Exception:
                malformed += 1
                continue
            total += 1
            messages = item.get("messages", []) if isinstance(item, dict) else []
            for m in messages if isinstance(messages, list) else []:
                if isinstance(m, dict):
                    role_counts[str(m.get("role"))] += 1
            length_counts[str(len(messages))] += 1
            reasons = inspect_conversation(item if isinstance(item, dict) else {})
            normalized, register = normalize_pronouns(messages if isinstance(messages, list) else [])
            # Duplicate detection uses normalized role/content, preserving the first occurrence.
            fingerprint = hashlib.sha256(json.dumps(normalized, ensure_ascii=False, sort_keys=True).encode()).hexdigest()
            if fingerprint in seen_hashes:
                reasons.append("duplikat_setelah_normalisasi")
            else:
                seen_hashes.add(fingerprint)
            record = {
                "id": f"intisari-v4-{line_no:06d}",
                "source": "INTISARI/intisari-indonesian-chat-v4",
                "source_line": line_no,
                "register": register,
                "messages": normalized,
            }
            if reasons:
                quarantined += 1
                reason_counts.update(reasons)
                record["review_reasons"] = sorted(set(reasons))
                quarantine.write(json.dumps(record, ensure_ascii=False) + "\n")
                if len(review_samples) < 500 and any(
                    x in reasons for x in ("campuran_register_awal", "susunan_kalimat_janggal",
                                           "jawaban_mengulang_pengguna", "pola_teks_mencurigakan", "label_pembicara_di_dalam_teks")
                ):
                    review_samples.append(record)
            else:
                candidate_count += 1
                record["status"] = "candidate_unreviewed_not_training_ready"
                cand.write(json.dumps(record, ensure_ascii=False) + "\n")

    review_path.write_text(
        "".join(json.dumps(x, ensure_ascii=False) + "\n" for x in review_samples),
        encoding="utf-8",
    )
    report = {
        "dataset": "INTISARI/intisari-indonesian-chat-v4",
        "input_file": input_path.name,
        "input_bytes": input_path.stat().st_size,
        "input_sha256": hashlib.sha256(input_path.read_bytes()).hexdigest(),
        "records_processed": total,
        "malformed_json_lines": malformed,
        "candidate_unreviewed_not_training_ready": candidate_count,
        "quarantined_for_review_or_exclusion": quarantined,
        "role_counts": dict(role_counts),
        "conversation_length_distribution": dict(length_counts),
        "reason_counts": dict(reason_counts.most_common()),
        "manual_review_sample_count": len(review_samples),
        "normalization": "consistent aku-kamu or saya-Anda per conversation",
        "training_use": "disabled_until_semantic_review_and_explicit_approval",
        "warning": "Candidate output has only passed conservative mechanical checks; it is NOT approved training data.",
    }
    (output_dir / "curation_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return report

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="data/external/intisari_v4/intisari_v4.jsonl")
    parser.add_argument("--output-dir", default="artifacts/intisari_v4")
    parser.add_argument("--limit", type=int, default=None)
    args = parser.parse_args()
    report = process(Path(args.input), Path(args.output_dir), args.limit)
    print(json.dumps(report, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
