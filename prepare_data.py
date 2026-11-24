"""Build a conservative Indonesian chatbot corpus and separate dialogue scenarios."""
import argparse, hashlib, html, json, random, re, unicodedata
from collections import Counter
from pathlib import Path
from datasets import load_dataset

WORD_RE = re.compile(r"[A-Za-zÀ-ÿ]+(?:['’-][A-Za-zÀ-ÿ]+)?")
SPEAKER_RE = re.compile(r"(?<![\w])([A-Z][A-Za-zÀ-ÿ0-9_-]{1,24}):\s*")
COMMON = set("""aku saya kamu anda gue gua gw lu lo elu dia mereka kita kami kalian ini itu yang dan di ke dari untuk dengan pada ada enggak nggak gak tidak iya ya bukan bisa mau akan sudah belum lagi aja saja sih dong deh kok nih tuh banget kalau kalo karena jadi tapi atau juga masih udah harus boleh jangan coba tolong makasih maaf apa siapa kapan dimana ke mana bagaimana kenapa gimana berapa hari tadi sekarang nanti besok kemarin pagi siang sore malam waktu jam rumah kerja sekolah kuliah teman keluarga orang anak ibu bapak ayah kakak adik makan minum tidur pergi pulang datang lihat dengar bilang cerita tanya jawab tahu ngerti paham pikir rasa suka cari kasih ambil buat bikin pakai jalan naik turun beli bayar harga murah mahal bagus enak capek senang sedih takut bingung mungkin kayak seperti memang cuma cukup dulu baru setelah sebelum biar supaya ternyata sempat terus""".split())
BAD = ("pada suatu ketika","di sebuah negeri yang jauh","dapat disimpulkan bahwa","seperti yang telah disebutkan","oleh karena itu dapat","secara komprehensif","mengejawantahkan","paradigma","berdasarkan uraian di atas")
ENGLISH = set("the and is are was were be been being of to for from with without this that these those you your we our they their he she his her as at by on in into about could would should".split())
RISKY_TOPIC = re.compile(
    r"\b(dokter|obat|dosis|gejala|penyakit|demam|bayi|hamil|kesehatan|sakit gigi|panadol|paracetamol|antibiotik|veteriner|kucing sakit|"
    r"investasi|reksa dana|saham|pinjaman|paylater|pajak|hukum|legal|kontrak|asuransi|utang|kredit|bunga bank|jaminan|sewa ruko|"
    r"kebakaran|listrik meledak|racun|bahan kimia|senjata|nyontek|bocoran ujian)\b", re.I)
# Reject assistant turns that invent a human life, physical presence, past experience, or personal schedule.
ASSISTANT_PERSONAL_CLAIM = re.compile(
    r"\b(?:gw|gue|gua|aku|saya)\b.{0,100}\b(?:pernah|tadi|kemarin|barusan|lagi|sedang|biasanya|sering|"
    r"udah|sudah|di\s+(?:warung|kantor|rumah|kos|jalan|sini|sana)|wfh|wfo|meeting|mampir|nongkrong|"
    r"ikut|datang|jemput|antar|beli|naik|nginep|nginap|masak|punya|kenal|nunggu|berangkat|standby|"
    r"nyampe|otw|siap\s+datang|ikut\s+bareng|bantuin\s+lu)\b", re.I)
ASSISTANT_FALSE_PRESENCE = re.compile(
    r"\b(?:gw|gue|gua|aku|saya)\b.{0,100}\b(?:ke\s+sana|datang|nyampe|temenin|jemput|antar|"
    r"bikinin|di\s+kos|di\s+rumah|lagi\s+nunggu|lagi\s+di\s+sini|sampe\s+sana|standby)\b", re.I)
SPECIFIC_UNVERIFIED = re.compile(
    r"(?:\bRp\.?\s?[\d.,]+|\b\d[\d.,]*\s?(?:rb|ribu|jt|juta)\b|\b(?:Jl\.?|Jalan)\s+[A-Z])", re.I)
REPETITIVE_CASUAL = re.compile(r"\b(gas|santai aja|wkwk|mantap|cuy|bre|anjir)\b", re.I)

def clean(value):
    value = html.unescape(str(value))
    value = re.sub(r"<[^>]+>|https?://\S+|www\.\S+", " ", value)
    value = unicodedata.normalize("NFKC", value)
    value = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", " ", value)
    return re.sub(r"\s+", " ", value).strip()

def get_messages(row):
    raw = row.get("conversations") or row.get("messages")
    if not isinstance(raw, list): return []
    out = []
    for item in raw:
        if not isinstance(item, dict): continue
        role = str(item.get("role", "")).lower().strip()
        text = item.get("content", "")
        if isinstance(text, list):
            text = " ".join(str(x.get("text", "")) if isinstance(x, dict) else str(x) for x in text)
        text = clean(text)
        if role in {"user", "assistant"} and text: out.append((role, text))
    return out

def scenario_messages(row):
    raw = clean(row.get("dialogue", ""))
    matches = list(SPEAKER_RE.finditer(raw))
    if len(matches) < 2: return []
    names, out = [], []
    for i, match in enumerate(matches):
        name = match.group(1).lower()
        if name not in names: names.append(name)
        end = matches[i+1].start() if i+1 < len(matches) else len(raw)
        out.append((f"speaker{names.index(name)+1}", clean(raw[match.end():end])))
    return out

def valid_turn(text):
    words = WORD_RE.findall(text.lower())
    if not 3 <= len(words) <= 60 or len(text) > 360: return False, "turn_length"
    low = text.lower()
    if any(p in low for p in BAD): return False, "formal_story_phrase"
    if sum(len(w) >= 16 for w in words) > 1: return False, "long_word_noise"
    if sum(w in ENGLISH for w in words)/len(words) > .18: return False, "english_heavy"
    if sum(c.isdigit() for c in text)/max(1,len(text)) > .12: return False, "digit_heavy"
    if sum(not c.isalnum() and not c.isspace() and c not in ".,!?'-" for c in text)/max(1,len(text)) > .08: return False, "symbol_noise"
    if re.search(r"(.)\1{4,}", text): return False, "character_spam"
    if len(set(words))/len(words) < .48: return False, "repetitive_words"
    common = sum(w in COMMON for w in words)
    if common < 1 or common/len(words) < .08: return False, "low_common_word_ratio"
    return True, "accepted"

def normalize(messages, scenario=False):
    if not 2 <= len(messages) <= 48: return None, "turn_count"
    clean_msgs = []
    for role, text in messages:
        text = clean(text)
        ok, reason = valid_turn(text)
        if not ok: return None, reason
        clean_msgs.append((role,text))
    if len({t.lower() for _,t in clean_msgs}) < 2: return None, "duplicate_turns"
    if not scenario and not {"user","assistant"}.issubset({r for r,_ in clean_msgs}):
        return None, "missing_role"
    lines = []
    for role,text in clean_msgs:
        label = ("Pembicara " + role.replace("speaker","")) if scenario else ("Pengguna" if role=="user" else "Asisten")
        lines.append(f"{label}: {text}")
    doc = "\n".join(lines)
    n = len(WORD_RE.findall(doc))
    if not 12 <= n <= 600: return None, "conversation_word_count"
    return doc, "accepted"

def conversation_quality(messages, source):
    # Public-source samples still contain fabricated assistant experiences and unsupported claims.
    # Hold this source for human review rather than admitting any row automatically.
    if source == "lorth_chat":
        return "manual_review_required"
    assistant_text = " ".join(text for role, text in messages if role == "assistant")
    full_text = " ".join(text for _, text in messages)
    if RISKY_TOPIC.search(full_text): return "risky_topic"
    if ASSISTANT_PERSONAL_CLAIM.search(assistant_text): return "assistant_personal_claim"
    if ASSISTANT_FALSE_PRESENCE.search(assistant_text): return "assistant_false_persona"
    if SPECIFIC_UNVERIFIED.search(assistant_text): return "assistant_unverified_specifics"
    if len(REPETITIVE_CASUAL.findall(assistant_text)) >= 4: return "repetitive_casual_style"
    return "accepted"

def source_rows():
    ds = load_dataset("LorthGyu/indonesian-chat", split="train")
    for row in ds:
        if str(row.get("style", "")).lower() == "formal": continue
        yield "lorth_chat", "chat", get_messages(row)
    scenarios = load_dataset("LorthGyu/indonesian-dialogue-scenarios", split="train")
    for row in scenarios:
        yield "lorth_scenarios", "scenario", scenario_messages(row)

def synthetic_candidate_docs(data_dir=Path("data/synthetic")):
    """Format synthetic JSONL conversations as candidates, never as approved training data."""
    docs, seen_ids = [], set()
    for path in sorted(Path(data_dir).glob("*.jsonl")):
        for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if not line.strip():
                continue
            row = json.loads(line)
            rid = row.get("id")
            messages = row.get("messages")
            if not isinstance(rid, str) or not rid or rid in seen_ids:
                raise ValueError(f"Invalid or duplicate synthetic id in {path.name}:{line_no}: {rid!r}")
            seen_ids.add(rid)
            if not isinstance(messages, list) or len(messages) < 4 or len(messages) > 16:
                raise ValueError(f"Invalid synthetic message count in {path.name}:{line_no}")
            roles = [m.get("role") if isinstance(m, dict) else None for m in messages]
            if roles[0] != "user" or roles[-1] != "assistant" or any(
                roles[i] == roles[i-1] or roles[i] not in {"user", "assistant"}
                for i in range(1, len(roles))
            ):
                raise ValueError(f"Invalid synthetic role order in {path.name}:{line_no}")
            lines = []
            for message in messages:
                content = clean(message.get("content", ""))
                if not content or len(WORD_RE.findall(content)) > 70 or len(content) > 420:
                    raise ValueError(f"Invalid synthetic turn in {path.name}:{line_no}")
                label = "Pengguna" if message["role"] == "user" else "Asisten"
                lines.append(f"{label}: {content}")
            docs.append("\n".join(lines))
    return docs


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--output",default="data/train.txt")
    p.add_argument("--samples",type=int,default=100)
    p.add_argument("--seed",type=int,default=20261124)
    p.add_argument("--synthetic-only",action="store_true",help="Use only the audited synthetic conversation candidates.")
    a=p.parse_args()
    accepted=[]; seen=set(); stats=Counter(); by_source={}; scenario_docs=[]
    for source,kind,messages in ([] if a.synthetic_only else source_rows()):
        stats[f"{source}.rows"]+=1
        doc,reason=normalize(messages,kind=="scenario")
        if not doc:
            stats[f"{source}.{reason}"]+=1
            continue
        if kind == "scenario":
            scenario_docs.append(doc)
            stats["lorth_scenarios.separated_for_review"]+=1
            continue
        reason=conversation_quality(messages,source)
        stats[f"{source}.{reason}"]+=1
        if reason != "accepted": continue
        digest=hashlib.sha256(doc.lower().encode()).hexdigest()
        if digest in seen: stats[f"{source}.duplicate"]+=1; continue
        seen.add(digest); accepted.append((source,doc)); by_source.setdefault(source,[]).append(doc)
    synthetic_docs = synthetic_candidate_docs()
    for doc in synthetic_docs:
        digest=hashlib.sha256(doc.lower().encode()).hexdigest()
        if digest in seen:
            stats["synthetic_candidate.duplicate"]+=1
            continue
        seen.add(digest)
        accepted.append(("synthetic_candidate",doc))
        stats["synthetic_candidate.accepted"]+=1
    out=Path(a.output); out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text("\n\n".join(doc for _,doc in accepted)+"\n" if accepted else "",encoding="utf-8")
    audit=Path("audit"); audit.mkdir(exist_ok=True)
    rng=random.Random(a.seed); samples=[]
    for source,docs in sorted(by_source.items()):
        docs=list(docs); rng.shuffle(docs)
        samples.append(f"===== {source}: {len(docs)} accepted =====")
        for i,doc in enumerate(docs[:a.samples],1): samples.append(f"\n[{i}]\n{doc}")
    (audit/"samples_by_source.txt").write_text("\n".join(samples)+"\n",encoding="utf-8")
    scenario_path=audit/"scenario_candidates.txt"
    scenario_path.write_text("\n\n".join(scenario_docs)+"\n" if scenario_docs else "",encoding="utf-8")
    report={"corpus_type":"multi_turn_indonesian_chatbot_conversation","sources":["LorthGyu/indonesian-chat","data/synthetic/*.jsonl"],"candidate_breakdown":{"synthetic_candidate_conversations":len(synthetic_docs),"public_source_accepted_conversations":sum(1 for source,_ in accepted if source != "synthetic_candidate")},"separated_sources":{"LorthGyu/indonesian-dialogue-scenarios":{"count":len(scenario_docs),"file":"scenario_candidates.txt","training_use":"excluded from chatbot base corpus pending role mapping and manual review"}},"excluded_sources":{"LorthGyu/indonesian-chat":"All normalized rows held for manual review after spot checks found fabricated assistant experiences, false physical presence, and unsupported specific claims.","daruokta/t5gemma2-indonesia-chat-formatted (chat_multiturn)":"Excluded pending separate quality review."},"quality_filters":["entire LorthGyu/indonesian-chat source held for manual review; no rows admitted automatically","turn-level Indonesian and noise checks","health/finance/legal/safety/cheating topic exclusion","assistant invented personal experience and physical presence exclusion","assistant unverified exact price/address claims exclusion","repetitive casual catchphrase exclusion"],"accepted_conversations":len(accepted),"total_words":sum(len(WORD_RE.findall(d)) for _,d in accepted),"source_and_filter_counts":dict(sorted(stats.items())),"samples_file":"samples_by_source.txt","training_ready":False,"candidate_status":"candidate_only_manual_review_required","candidate_file":str(out),"training_use":"disabled pending manual review and explicit approval","note":"Automated filters are conservative but cannot guarantee factuality or naturalness; manual sample review is mandatory."}
    (audit/"report.json").write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
    print(json.dumps(report,ensure_ascii=False,indent=2))
    print("Candidate chatbot corpus created. Scenario dialogues are separated and training remains disabled.")

if __name__=="__main__": main()
