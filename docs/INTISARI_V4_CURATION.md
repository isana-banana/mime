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
- `candidate_unreviewed.jsonl`: conversations that pass mechanical checks. Still unreviewed and NOT training-ready.
- `quarantine.jsonl`: conversations with structural, digital-topic, lexical, repetition, length, or other review flags.
- `manual_review_sample.jsonl`: a small sample of flagged records for human inspection.
- `curation_report.json`: counts, source hash, and reasons.

## Curation policy
- Keep the raw source unchanged.
- Normalize pronouns consistently per conversation: casual `aku-kamu` or polite `saya-Anda`.
- Remove digital-topic conversations from the candidate pool.
- Quarantine malformed, repetitive, structurally broken, or suspicious conversations.
- **A fictional assistant persona is allowed.** Do not reject or downgrade a conversation merely because the assistant says it has a body, job, family, friends, pets, preferences, possessions, routines, or personal experiences. These details may be part of the chatbot's conversational character.
- Review persona details for coherence within the dialogue. Correct genuine contradictions, confusing chronology, or replies that do not answer the user; do not treat ordinary first-person storytelling as a defect.
- During editing, preserve the source's intended persona and meaning. Do not invent extra biographical details, locations, numbers, or events just to fill gaps.
- Judge factual accuracy when the assistant gives real-world information or advice. Fictional persona storytelling is evaluated for internal consistency and conversational relevance, not as a claim about a real assistant.
- Never equate mechanical filtering with semantic quality. Every candidate still needs human review for relevance, naturalness, coherence, factual soundness where applicable, and useful assistant behavior.
- Do not use these outputs for training until semantic review is complete and the user explicitly approves training.

## Important
This workflow is intentionally separate from MIME training. It does not train a model,
modify the existing 448-conversation synthetic corpus, or publish a training artifact.
