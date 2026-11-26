# INTISARI V4 — Audit Mutu Tahap 3, Batch 1 (20 percakapan)

- Branch: `experiment/intisari-v4-curation`
- Sumber: `stage3_needs_human_review.jsonl` dari pemrosesan penuh 50.047 baris.
- Batch: 20 ID terpilih dari antrean pemeriksaan mutu.
- Persona asisten (keluarga, pekerjaan, hewan, pengalaman, kendaraan, dan kesukaan) tetap diperbolehkan.

## Hasil

| Keputusan | Jumlah |
|---|---:|
| `rewrite` | 13 |
| `discard` | 4 |
| `discard_structure` | 3 |
| `keep_light_edit` | 0 |
| `exclude_topic` | 0 |
| **Total** | **20** |

## Ringkasan penyuntingan

- Contoh yang masih dapat diselamatkan ditulis ulang dengan bahasa sehari-hari, alur yang jelas, dan jawaban yang menanggapi pesan sebelumnya.
- Contoh yang dibuang memiliki makna rusak berat, pengulangan yang mendominasi, placeholder, atau struktur giliran yang tidak dapat dipulihkan.
- Tidak ada contoh yang dibuang hanya karena asisten mengaku punya hewan, kendaraan, pekerjaan, atau pengalaman.
- Semua hasil masih `training_ready=false`; batch ini belum merupakan persetujuan untuk training.

## ID yang diaudit

- intisari-v4-044458 — `rewrite`
- intisari-v4-042035 — `rewrite`
- intisari-v4-003105 — `discard_structure`
- intisari-v4-027948 — `discard`
- intisari-v4-030784 — `rewrite`
- intisari-v4-021466 — `rewrite`
- intisari-v4-028135 — `rewrite`
- intisari-v4-009792 — `discard`
- intisari-v4-038510 — `rewrite`
- intisari-v4-032215 — `rewrite`
- intisari-v4-012283 — `discard_structure`
- intisari-v4-034609 — `rewrite`
- intisari-v4-035010 — `discard`
- intisari-v4-019524 — `rewrite`
- intisari-v4-037274 — `rewrite`
- intisari-v4-046294 — `rewrite`
- intisari-v4-022674 — `rewrite`
- intisari-v4-037495 — `discard_structure`
- intisari-v4-024758 — `rewrite`
- intisari-v4-034293 — `discard`
