# INTISARI V4 curation lane

This branch contains a conservative, reproducible curation pipeline for the raw
INTISARI V4 source. The original JSONL file is treated as immutable source data.

## Input
`data/external/intisari_v4/intisari_v4.jsonl`

Source: https://huggingface.co/datasets/INTISARI/intisari-indonesian-chat-v4

## Run locally
```bash
python curate_intisari_v4.py \
  --input data/external/intisari_v4/intisari_v4.jsonl \
  --output-dir artifacts/intisari_v4
```

## Outputs
- `candidate_unreviewed.jsonl`: conversations that pass mechanical checks and have consistent pronouns. Still unreviewed and NOT training-ready.
- `quarantine.jsonl`: conversations with structural, digital-topic, lexical, repetition, length, or other review flags.
- `manual_review_sample.jsonl`: a small sample of flagged records for human inspection.
- `curation_report.json`: counts, source hash, and reasons.

## Curation policy
- Keep the raw source unchanged.
- Normalize pronouns consistently per conversation: casual `aku-kamu` or polite `saya-Anda`.
- Remove digital-topic conversations from the candidate pool.
- Quarantine malformed, repetitive, structurally broken, or suspicious conversations.
- Never equate mechanical filtering with semantic quality. Every candidate still needs a human quality review for relevance, naturalness, coherence, factual soundness, and useful assistant behavior.
- Do not use these outputs for training until semantic review is complete and the user explicitly approves training.

## Important
This workflow is intentionally separate from MIME training. It does not train a model,
modify the existing 448-conversation synthetic corpus, or publish a training artifact.
