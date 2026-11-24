"""Build a quality-first Indonesian conversation corpus from curated open datasets."""
import argparse, hashlib, html, json, random, re, unicodedata
from collections import Counter
from pathlib import Path
from datasets import load_dataset

WORD_RE = re.compile(r"[A-Za-zÀ-ÿ]+(?:['’-][A-Za-zÀ-ÿ]+)?")
SPEAKER_RE = re.compile(r"(?<![\w])([A-Z][A-Za-zÀ-ÿ0-9_-]{1,24}):\s*")
COMMON = set("""aku saya kamu anda gue gua gw lu lo elu dia mereka kita kami kalian ini itu yang dan di ke dari untuk dengan pada ada enggak nggak gak tidak iya ya bukan bisa mau akan sudah belum lagi aja saja sih dong deh kok nih tuh banget kalau kalo karena jadi tapi atau juga masih udah harus boleh jangan coba tolong makasih maaf apa siapa kapan dimana ke mana bagaimana kenapa gimana berapa hari tadi sekarang nanti besok kemarin pagi siang sore malam waktu jam rumah kerja sekolah kuliah teman keluarga orang anak ibu bapak ayah kakak adik makan minum tidur pergi pulang datang lihat dengar bilang cerita tanya jawab tahu ngerti paham pikir rasa suka cari kasih ambil buat bikin pakai jalan naik turun beli bayar harga murah mahal bagus enak capek senang sedih takut bingung mungkin kayak seperti memang cuma cukup dulu baru setelah sebelum biar supaya ternyata sempat terus""".split())
BAD = ("pada suatu ketika","di sebuah negeri yang jauh","dapat disimpulkan bahwa","seperti yang telah disebutkan","oleh karena itu dapat","secara komprehensif","mengejawantahkan","paradigma","berdasarkan uraian di atas")
ENGLISH = set("the and is are was were be been being of to for from with without this that these those you your we our they their he she his her as at by on in into about could would should".split())
# Exclude domains where short synthetic answers can teach unsafe or misleading advice.
RISKY_TOPIC = re.compile(
    r"\\b(dokter|obat|dosis|gejala|penyakit|demam|bayi|hamil|kesehatan|"
    r"sakit gigi|panadol|paracetamol|antibiotik|veteriner|kucing sakit|"
    r investasi|reksa dana|saham|pinjaman|paylater|pajak|hukum|legal|kontrak|"
    r"asuransi|utang|kredit|bunga bank|jaminan|sewa ruko|kebakaran|"
    r"listrik meledak|racun|bahan kimia|senjata|nyontek|bocoran ujian)\\b".replace("r investasi", "investasi"),
    re.I,
)
ASSISTANT_PHYSICAL = re.compile(
    r"\\b(gw|gue|gua|aku|saya)\\b.{0,90}\\b(ke sana|datang|nyampe|temenin|jemput|antar|"
    r"bikinin|di kos|di rumah|lagi nunggu|lagi di sini|chat pagi-pagi|sampe sana|standby)\\b",
    re.I,
)
REPETITIVE_CASUAL = re.compile(r"\\b(gas|santai aja|wkwk|mantap|cuy|bre)\\b", re.I)


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
    full_text = " ".join(text for _, text in messages)
    if RISKY_TOPIC.search(full_text):
        return "risky_topic"
    if source == "lorth_chat":
        assistant_text = " ".join(text for role, text in messages if role == "assistant")
        if ASSISTANT_PHYSICAL.search(assistant_text):
            return "assistant_false_persona"
        casual_hits = len(REPETITIVE_CASUAL.findall(assistant_text))
        if casual_hits >= 5:
            return "repetitive_casual_style"
    return "accepted"

def source_rows():
    specs = [
        ("lorth_chat","LorthGyu/indonesian-chat",None,"chat"),
        ("lorth_scenarios","LorthGyu/indonesian-dialogue-scenarios",None,"scenario"),
    ]
    for name, repo, config, kind in specs:
        print(f"Loading {name}: {repo} {config or ''}")
        ds = load_dataset(repo, config, split="train") if config else load_dataset(repo, split="train")
        for row in ds:
            # This project targets everyday speech, so exclude explicitly formal
            # examples from the mixed-style source instead of diluting casual data.
            if name == "lorth_chat" and str(row.get("style", "")).lower() == "formal":
                continue
            yield name, kind, scenario_messages(row) if kind=="scenario" else get_messages(row)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--output",default="data/train.txt")
    p.add_argument("--samples",type=int,default=100)
    p.add_argument("--seed",type=int,default=20261124)
    a=p.parse_args()
    accepted=[]; seen=set(); stats=Counter(); by_source={}
    for source,kind,messages in source_rows():
        stats[f"{source}.rows"]+=1
        doc,reason=normalize(messages,kind=="scenario")
        if doc:
            reason = conversation_quality(messages, source)
        stats[f"{source}.{reason}"]+=1
        if not doc or reason != "accepted": continue
        digest=hashlib.sha256(doc.lower().encode()).hexdigest()
        if digest in seen: stats[f"{source}.duplicate"]+=1; continue
        seen.add(digest); accepted.append((source,doc)); by_source.setdefault(source,[]).append(doc)
    # Corpus construction floor only; human review is still required before training.
    # The audit report deliberately keeps training_ready=false.
    if not accepted:
        raise RuntimeError("No conversations survived the quality filters; inspect audit rules and source data.")
    out=Path(a.output); out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text("\n\n".join(doc for _,doc in accepted)+"\n",encoding="utf-8")
    audit=Path("audit"); audit.mkdir(exist_ok=True)
    rng=random.Random(a.seed); samples=[]
    for source,docs in sorted(by_source.items()):
        docs=list(docs); rng.shuffle(docs)
        samples.append(f"===== {source}: {len(docs)} accepted =====")
        for i,doc in enumerate(docs[:a.samples],1): samples.append(f"\n[{i}]\n{doc}")
    (audit/"samples_by_source.txt").write_text("\n".join(samples)+"\n",encoding="utf-8")
    report={"corpus_type":"multi_turn_indonesian_conversation","sources":["LorthGyu/indonesian-chat","LorthGyu/indonesian-dialogue-scenarios"],"excluded_sources":{"daruokta/t5gemma2-indonesia-chat-formatted (chat_multiturn)":"Excluded from the base conversational corpus: samples are predominantly long scripted tutorials and include higher-risk factual advice; may be reconsidered as a separately reviewed task dataset."},"quality_filters":["turn-level Indonesian and noise checks","conversation-level health/finance/legal/safety/cheating topic exclusion","assistant false-physical-presence exclusion for Lorth chat","repetitive casual catchphrase exclusion"],"accepted_conversations":len(accepted),"total_words":sum(len(WORD_RE.findall(d)) for _,d in accepted),"source_and_filter_counts":dict(sorted(stats.items())),"samples_file":"samples_by_source.txt","training_ready":False,"note":"Human review of random samples is required before training."}
    (audit/"report.json").write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
    print(json.dumps(report,ensure_ascii=False,indent=2))
    print("Candidate corpus created. Review audit/samples_by_source.txt before enabling training.")

if __name__=="__main__": main()
