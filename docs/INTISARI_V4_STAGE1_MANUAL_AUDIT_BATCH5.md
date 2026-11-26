# INTISARI V4 — Audit Manual Relevansi Tahap 1, Batch 5 (25 percakapan)

- Sumber: `stage1_mixed_context_review.jsonl` dari hasil pemrosesan penuh.
- Batch ini dipilih setelah mencocokkan ID dengan empat batch sebelumnya agar tidak mengulang ID yang sudah diperiksa.
- Prinsip: topik luring tetap dipertahankan jika internet, email, website, atau aplikasi hanya disebut sebagai alat bantu. Topik gim, media sosial, layanan internet, dan belanja daring sebagai pokok percakapan dikeluarkan.

## Hasil

| Keputusan | Jumlah |
|---|---:|
| Tetap dalam cakupan | 11 |
| Keluarkan sebagai topik digital | 14 |
| **Total** | **25** |

## Catatan penting

- Percakapan pasar, resep, makan siang, promo mal, perjalanan, pekerjaan, dan pengurusan dokumen tetap dipertahankan.
- Jawaban yang mengalihkan pengguna dari pasar ke Google/supermarket atau memberi rute perjalanan yang tidak masuk akal akan diperbaiki pada tahap mutu.
- Belanja daring yang menjadi inti dialog, gim daring, dan media sosial tetap dikeluarkan.
- Batch ini menambah 25 ID unik yang sebelumnya belum diaudit.

## ID yang diperiksa

- intisari-v4-002092 — `exclude_digital_topic`
- intisari-v4-002250 — `keep_in_scope`
- intisari-v4-002383 — `exclude_digital_topic`
- intisari-v4-002460 — `keep_in_scope`
- intisari-v4-002495 — `keep_in_scope`
- intisari-v4-002497 — `keep_in_scope`
- intisari-v4-002650 — `exclude_digital_topic`
- intisari-v4-002778 — `keep_in_scope`
- intisari-v4-002794 — `exclude_digital_topic`
- intisari-v4-002866 — `exclude_digital_topic`
- intisari-v4-002907 — `exclude_digital_topic`
- intisari-v4-002923 — `exclude_digital_topic`
- intisari-v4-002986 — `exclude_digital_topic`
- intisari-v4-003019 — `exclude_digital_topic`
- intisari-v4-003044 — `keep_in_scope`
- intisari-v4-003047 — `keep_in_scope`
- intisari-v4-003049 — `keep_in_scope`
- intisari-v4-003174 — `keep_in_scope`
- intisari-v4-003315 — `exclude_digital_topic`
- intisari-v4-003349 — `exclude_digital_topic`
- intisari-v4-003353 — `exclude_digital_topic`
- intisari-v4-003410 — `keep_in_scope`
- intisari-v4-003411 — `keep_in_scope`
- intisari-v4-003445 — `exclude_digital_topic`
- intisari-v4-003447 — `exclude_digital_topic`

Semua keputusan masih `training_ready=false`.
