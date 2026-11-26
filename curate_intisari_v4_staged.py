#!/usr/bin/env python3
"""Three-stage, non-destructive INTISARI V4 preparation for MIME.

Stage 1: exclude clearly out-of-scope digital-topic conversations.
Stage 2: normalize gue/gua/gw and lo/lu/elo/elu to aku-kamu.
Stage 3: flag quality issues for human editing or exclusion.
No output is marked training-ready.
"""
from __future__ import annotations
import argparse, collections, hashlib, json, re
from pathlib import Path
from typing import Any

# Deliberately narrow: ordinary in-person shopping, markets, malls and stores stay in scope.
DIGITAL_PATTERNS = {
    "internet_web": r"\b(?:internet|website|situs web|browser|wifi|wi-fi)\b",
    "social_media": r"\b(?:media sosial|sosial media|medsos|sosmed|instagram|facebook|twitter|tiktok|youtube)\b",
    "apps_accounts": r"\b(?:aplikasi|app|login|logout|kata sandi|password|username|akun digital|kode verifikasi|whatsapp|email|e-mail)\b",
    "computing_devices": r"\b(?:komputer|laptop|ponsel|smartphone|handphone|telepon genggam|tablet|gadget|keyboard|printer|prosesor|processor|samsung|iphone|android)\b",
    "digital_services": r"\b(?:marketplace|e-commerce|ecommerce|toko online|belanja online|online shop|online shopping|streaming|chatbot|layanan daring|platform digital)\b",
    "digital_games": r"\b(?:game online|video game|game mobile|game pc|mobile legends|pubg|main game|bermain game)\b",
    "computing_topics": r"\b(?:data mining|komputasi|algoritma|pemrograman|coding|kode program|basis data|database)\b",
    "digital_presentation": r"\b(?:slide presentasi|presentasi digital|powerpoint|kode html)\b",
}
DIGITAL_RE = {k: re.compile(v, re.I) for k,v in DIGITAL_PATTERNS.items()}
# These terms can occur in ordinary offline life; they are reviewed, never auto-excluded.
AMBIGUOUS_PATTERNS = {
    "presentasi": re.compile(r"\b(?:presentasi|slide)\b", re.I),
    "kamera_layar": re.compile(r"\b(?:kamera|layar|video|televisi|tv)\b", re.I),
}
SLANG_MAP = {
    "gue":"aku", "gua":"aku", "gw":"aku",
    "lo":"kamu", "lu":"kamu", "elo":"kamu", "elu":"kamu",
    "saya":"aku", "anda":"kamu",
}
SLANG_RE = re.compile(r"\b(?:gue|gua|gw|lo|lu|elo|elu)\b", re.I)
WORD_RE = re.compile(r"\b([\w]+)(?:\s+\1){1,}\b", re.I)
PLACEHOLDER_RE = re.compile(r"(?:\.{3,}|\[/?(?:nama|jawaban|isi|teks)\])", re.I)
BROKEN_WORDS = {"baikaa","sedanggri","keterpaskan","mereko","sarankin","pertaya","kuliyah","ngaburuhu","dangdang","gesum","pemeranakan"}
BROKEN_RE = re.compile(r"\b(?:" + "|".join(map(re.escape, sorted(BROKEN_WORDS))) + r")\b", re.I)
GIBBERISH_RE = re.compile(r"\b[A-Za-z]{22,}\b")

def load_jsonl(path: Path):
    with path.open(encoding="utf-8") as f:
        for line_no, line in enumerate(f, 1):
            try:
                item=json.loads(line)
            except Exception:
                yield line_no, None
                continue
            yield line_no, item

def messages_of(item: Any):
    return item.get("messages", []) if isinstance(item, dict) else []

def text_of(messages):
    return " ".join(str(m.get("content","")) for m in messages if isinstance(m,dict))

def write_jsonl(path: Path, records):
    with path.open("w",encoding="utf-8") as f:
        for x in records:
            f.write(json.dumps(x,ensure_ascii=False)+"\n")

def stage1(input_path: Path, out: Path):
    in_scope=[]; excluded=[]; ambiguous=[]; malformed=0; categories=collections.Counter()
    for line_no,item in load_jsonl(input_path):
        if item is None:
            malformed+=1; continue
        msgs=messages_of(item); joined=text_of(msgs)
        hits=[name for name,pat in DIGITAL_RE.items() if pat.search(joined)]
        amb=[name for name,pat in AMBIGUOUS_PATTERNS.items() if pat.search(joined)]
        rec={"id":f"intisari-v4-{line_no:06d}","source_line":line_no,"messages":msgs}
        if hits:
            rec["stage1_decision"]="exclude_digital_topic"
            rec["stage1_reasons"]=hits
            excluded.append(rec); categories.update(hits)
        else:
            rec["stage1_decision"]="in_scope_pending_quality_review"
            if amb:
                rec["stage1_ambiguous_terms"]=amb
                ambiguous.append({"id":rec["id"],"terms":amb,"messages":msgs})
            in_scope.append(rec)
    write_jsonl(out/"stage1_in_scope.jsonl",in_scope)
    write_jsonl(out/"stage1_excluded_digital.jsonl",excluded)
    write_jsonl(out/"stage1_ambiguous_review.jsonl",ambiguous)
    return {"source_records":len(in_scope)+len(excluded),"malformed_lines":malformed,
            "stage1_in_scope":len(in_scope),"excluded_digital":len(excluded),
            "ambiguous_records_also_kept_in_scope":len(ambiguous),
            "exclusion_reason_counts":dict(categories.most_common()),
            "training_ready":False}

def replace_words(text: str):
    pat=re.compile(r"\b("+"|".join(SLANG_MAP)+r")\b",re.I)
    changes=[]
    def sub(m):
        old=m.group(0); new=SLANG_MAP[old.lower()]
        if old[:1].isupper(): new=new.capitalize()
        changes.append((old,new))
        return new
    return pat.sub(sub,text),changes

def stage2(in_path: Path, out: Path):
    clean=[]; changed_records=0; changed_tokens=collections.Counter(); changed_ids=[]
    residual=collections.Counter()
    for _,item in load_jsonl(in_path):
        if item is None: continue
        msgs=messages_of(item); new_msgs=[]; record_changes=[]
        for m in msgs:
            if not isinstance(m,dict):
                new_msgs.append(m); continue
            content=str(m.get("content",""))
            new,changes=replace_words(content)
            m2=dict(m); m2["content"]=new; new_msgs.append(m2)
            record_changes.extend(changes)
        rec=dict(item); rec["messages"]=new_msgs
        if record_changes:
            changed_records+=1; changed_ids.append(rec.get("id"))
            for old,new in record_changes: changed_tokens[old.lower()]+=1
            rec["stage2_language_edit"]="slang_to_aku_kamu"
            rec["stage2_change_count"]=len(record_changes)
        else:
            rec["stage2_language_edit"]="no_gue_lo_slang_found"
        # Audit remaining variants after the replacement.
        joined=text_of(new_msgs)
        for m in SLANG_RE.findall(joined): residual[m.lower()]+=1
        clean.append(rec)
    write_jsonl(out/"stage2_language_normalized.jsonl",clean)
    return {"records_processed":len(clean),"records_changed":changed_records,
            "replacement_counts_by_original_word":dict(changed_tokens),
            "residual_slang_counts":dict(residual),"training_ready":False}

def stage3(in_path: Path, out: Path):
    review=[]; no_flag=[]; reasons=collections.Counter(); malformed=0
    for _,item in load_jsonl(in_path):
        if item is None:
            malformed+=1; continue
        msgs=messages_of(item); flags=[]
        roles=[m.get("role") if isinstance(m,dict) else None for m in msgs]
        contents=[str(m.get("content","")).strip() if isinstance(m,dict) else "" for m in msgs]
        joined=" ".join(contents)
        if len(msgs)<2 or not msgs or roles[0]!="user" or roles[-1]!="assistant" or any(roles[i]==roles[i-1] for i in range(1,len(roles))) or any(r not in ("user","assistant") for r in roles):
            flags.append("struktur_giliran")
        if any(not x for x in contents): flags.append("pesan_kosong")
        if PLACEHOLDER_RE.search(joined): flags.append("placeholder")
        if WORD_RE.search(joined): flags.append("pengulangan_kata")
        if BROKEN_RE.search(joined): flags.append("kata_rusak_dikenali")
        if GIBBERISH_RE.search(joined): flags.append("teks_mencurigakan")
        if len(msgs)>12: flags.append("terlalu_banyak_giliran")
        if len(joined)>2400: flags.append("terlalu_panjang")
        if any(len(x.split())<2 for x in contents): flags.append("pesan_sangat_pendek")
        if flags:
            rec=dict(item); rec["stage3_review_reasons"]=flags
            rec["stage3_status"]="needs_human_edit_or_discard"
            review.append(rec); reasons.update(flags)
        else:
            rec=dict(item); rec["stage3_status"]="no_obvious_mechanical_issue_still_needs_semantic_review"
            no_flag.append(rec)
    write_jsonl(out/"stage3_needs_human_review.jsonl",review)
    write_jsonl(out/"stage3_no_obvious_mechanical_issue.jsonl",no_flag)
    return {"records_processed":len(review)+len(no_flag),"malformed_lines":malformed,
            "needs_human_review":len(review),"no_obvious_mechanical_issue_not_semantically_approved":len(no_flag),
            "review_reason_counts":dict(reasons.most_common()),"training_ready":False}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--input",default="data/external/intisari_v4/intisari_v4.jsonl")
    p.add_argument("--output-dir",default="artifacts/intisari_v4_staged")
    a=p.parse_args()
    src=Path(a.input); out=Path(a.output_dir); out.mkdir(parents=True,exist_ok=True)
    reports={}
    reports["stage1"]=stage1(src,out)
    reports["stage2"]=stage2(out/"stage1_in_scope.jsonl",out)
    reports["stage3"]=stage3(out/"stage2_language_normalized.jsonl",out)
    reports["source_sha256"]=hashlib.sha256(src.read_bytes()).hexdigest()
    reports["policy"]="Stage 1 -> Stage 2 -> Stage 3; raw source immutable; no automatic training approval."
    (out/"three_stage_report.json").write_text(json.dumps(reports,ensure_ascii=False,indent=2),encoding="utf-8")
    print(json.dumps(reports,ensure_ascii=False,indent=2))
if __name__=="__main__": main()
