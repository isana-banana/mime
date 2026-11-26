# INTISARI V4 — Audit Manual Relevansi Tahap 1, Batch 1 (25 percakapan)

- Sumber: antrean `stage1_mixed_context_review.jsonl` dari pemrosesan penuh.
- Fokus: membedakan percakapan digital sebagai topik utama dari penyebutan digital yang hanya membantu percakapan luring.
- Aturan: pasar, warung, supermarket, mal, kegiatan memasak, olahraga, perjalanan, dan kehidupan sehari-hari tetap termasuk cakupan. Satu penyebutan website, email, YouTube, atau aplikasi tidak otomatis membuat percakapan luring menjadi topik digital.

## Hasil

| Keputusan | Jumlah |
|---|---:|
| Tetap dalam cakupan | 7 |
| Keluarkan sebagai topik digital | 18 |
| **Total** | **25** |

## Catatan keputusan

- Percakapan yang benar-benar membahas Zoom, Wi-Fi, media sosial, aplikasi musik, gim digital, atau belanja online dikeluarkan.
- Percakapan tentang makanan, resep, warung, dan promo mal tetap dipertahankan walaupun menyebut internet atau website sekilas.
- Contoh campuran yang dipertahankan dapat disunting pada tahap mutu agar kembali fokus pada topik luring.
- Audit batch ini hanya mencakup 25 dari 1.427 contoh campuran. Tahap 1 belum selesai secara manual.

## ID yang diperiksa

- intisari-v4-003042 — `keep_in_scope`
- intisari-v4-042856 — `exclude_digital_topic`
- intisari-v4-019560 — `exclude_digital_topic`
- intisari-v4-021986 — `keep_in_scope`
- intisari-v4-038697 — `exclude_digital_topic`
- intisari-v4-010283 — `exclude_digital_topic`
- intisari-v4-011902 — `exclude_digital_topic`
- intisari-v4-021169 — `exclude_digital_topic`
- intisari-v4-028843 — `keep_in_scope`
- intisari-v4-017254 — `exclude_digital_topic`
- intisari-v4-020409 — `exclude_digital_topic`
- intisari-v4-006853 — `exclude_digital_topic`
- intisari-v4-011423 — `keep_in_scope`
- intisari-v4-034108 — `keep_in_scope`
- intisari-v4-002843 — `keep_in_scope`
- intisari-v4-011757 — `exclude_digital_topic`
- intisari-v4-015311 — `exclude_digital_topic`
- intisari-v4-003357 — `exclude_digital_topic`
- intisari-v4-042147 — `exclude_digital_topic`
- intisari-v4-046237 — `keep_in_scope`
- intisari-v4-035693 — `exclude_digital_topic`
- intisari-v4-010410 — `exclude_digital_topic`
- intisari-v4-002078 — `exclude_digital_topic`
- intisari-v4-004529 — `exclude_digital_topic`
- intisari-v4-032836 — `exclude_digital_topic`

Semua keputusan masih `training_ready=false`.
