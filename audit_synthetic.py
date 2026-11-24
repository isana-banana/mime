"""Audit the original synthetic Indonesian dialogue batches without admitting them to training."""
import collections
import hashlib
import json
import re
from pathlib import Path

DATA = Path("data/synthetic")
OUT = Path("audit/synthetic_report.json")
ALLOWED_STYLES = {"casual_aku_kamu", "casual_saya_anda", "casual_gue_lo"}
RISKY = re.compile(r"\\b(dokter|obat|dosis|gejala|penyakit|demam|hamil|investasi|saham|pinjaman|pajak|hukum|kontrak|asuransi|utang|kredit|kebakaran|racun|senjata|nyontek)\\b", re.I)
SPECIFIC = re.compile(r"(?:\\bRp\\.?\\s?[\\d.,]+|\\b\\d[\\d.,]*\\s?(?:rb|ribu|jt|juta)\\b|\\b(?:Jl\\.?|Jalan)\\s+[A-Z])", re.I)
FAKE_PERSONA = re.compile(
    r"\\b(?:aku|saya|gue|gua|gw)\\b.{0,90}\\b(?:pernah|tadi|kemarin|barusan|nongkrong|mampir|"
    r"menjemput|jemput|mengantar|antar|datang ke|berangkat|sedang makan|lagi makan|di kantor|di warung|"
    r"di rumahku|rumah saya|temenin|menemani secara langsung)\\b", re.I
)
WORD = re.compile(r"[a-zA-ZÀ-ÿ]+(?:['’-][a-zA-ZÀ-ÿ]+)?")

def audit():
    files = sorted(DATA.glob("*.jsonl"))
    rows, issues, seen = [], [], {}
    for path in files:
        for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if not line.strip():
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError as exc:
                issues.append({"file": path.name, "line": line_no, "issue": f"invalid_json: {exc.msg}"})
                continue
            rows.append((path.name, line_no, row))

    ids, topics, styles, response_hashes = set(), collections.Counter(), collections.Counter(), collections.Counter()
    words = 0
    for filename, line_no, row in rows:
        where = {"file": filename, "line": line_no, "id": row.get("id")}
        def fail(reason):
            issues.append({**where, "issue": reason})
        rid = row.get("id")
        if not isinstance(rid, str) or not rid:
            fail("missing_id")
        elif rid in ids:
            fail("duplicate_id")
        else:
            ids.add(rid)
        topic, style = row.get("topic"), row.get("style")
        if not isinstance(topic, str) or not topic.strip():
            fail("missing_topic")
        else:
            topics[topic] += 1
        if style not in ALLOWED_STYLES:
            fail("unknown_style")
        else:
            styles[style] += 1
        messages = row.get("messages")
        if not isinstance(messages, list) or len(messages) < 4 or len(messages) > 16:
            fail("invalid_message_count")
            continue
        roles = [m.get("role") if isinstance(m, dict) else None for m in messages]
        if roles[0] != "user" or roles[-1] != "assistant" or any(
            roles[i] == roles[i-1] or roles[i] not in {"user", "assistant"}
            for i in range(1, len(roles))
        ):
            fail("invalid_role_order")
        contents = []
        for msg in messages:
            content = msg.get("content") if isinstance(msg, dict) else None
            if not isinstance(content, str) or not content.strip():
                fail("empty_or_invalid_content")
                continue
            content = re.sub(r"\\s+", " ", content).strip()
            contents.append(content)
            count = len(WORD.findall(content))
            words += count
            if count < 3 or count > 70 or len(content) > 420:
                fail("turn_length_out_of_range")
            if RISKY.search(content):
                fail("risky_topic")
            if msg.get("role") == "assistant":
                if FAKE_PERSONA.search(content):
                    fail("possible_fake_persona")
                if SPECIFIC.search(content):
                    fail("unverified_specific_detail")
        normalized = " ".join(contents).lower()
        digest = hashlib.sha256(normalized.encode()).hexdigest()
        if digest in seen:
            fail(f"duplicate_conversation_of_{seen[digest]}")
        else:
            seen[digest] = rid
        for msg in messages:
            if isinstance(msg, dict) and msg.get("role") == "assistant":
                answer = re.sub(r"[^a-zA-ZÀ-ÿ ]", "", msg.get("content", "").lower())
                response_hashes[hashlib.sha256(answer.encode()).hexdigest()] += 1

    total = len(rows)
    style_counts = dict(styles)
    topic_counts = dict(topics.most_common())
    repeated_answers = sum(n - 1 for n in response_hashes.values() if n > 1)
    report = {
        "files": [p.name for p in files],
        "conversation_count": total,
        "unique_ids": len(ids),
        "total_words": words,
        "topic_count": len(topics),
        "topic_distribution": topic_counts,
        "style_distribution": style_counts,
        "exact_repeated_assistant_answers": repeated_answers,
        "issue_count": len(issues),
        "issues": issues[:250],
        "training_ready": False,
        "decision": "manual_review_required" if total and not issues else "reject_or_repair",
        "note": "Structural and heuristic audit only; it cannot certify factual accuracy, usefulness, or naturalness."
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return report

if __name__ == "__main__":
    audit()
