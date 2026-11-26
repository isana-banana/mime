# Audit Ulang Persona Sampel Lama INTISARI V4 — Batch 5 (20 percakapan)

- Cabang: `experiment/intisari-v4-curation`
- Sumber: sampel manual 100 percakapan dari INTISARI V4.
- Cakupan batch ini: 20 ID berikutnya yang belum diaudit ulang.
- Kebijakan: persona asisten yang memiliki tubuh, keluarga, pekerjaan, hewan, selera, dan pengalaman pribadi diperbolehkan. Penilaian berfokus pada bahasa, konteks, relevansi, struktur, dan ketepatan informasi.

## Hasil

| Keputusan | Jumlah |
|---|---:|
| `keep_light_edit` | 3 |
| `rewrite` | 12 |
| `discard` | 3 |
| `exclude_topic` | 2 |
| `discard_structure` | 0 |
| **Total** | **20** |

## Catatan

- Dua contoh dikecualikan karena membahas akun/media sosial, sesuai batas topik digital.
- Dua contoh dibuang karena makna inti tidak dapat dipastikan dari teks yang rusak.
- Pengalaman, selera, atau latar pribadi asisten tidak menjadi alasan penolakan.
- Semua keputusan masih berstatus audit dan `training_ready=false`; belum ada persetujuan untuk pelatihan.

## ID yang diperiksa

- intisari-v4-020565 — `rewrite`
- intisari-v4-021040 — `rewrite`
- intisari-v4-022921 — `discard`
- intisari-v4-024374 — `rewrite`
- intisari-v4-025455 — `rewrite`
- intisari-v4-025977 — `keep_light_edit`
- intisari-v4-026460 — `exclude_topic`
- intisari-v4-026729 — `exclude_topic`
- intisari-v4-028040 — `rewrite`
- intisari-v4-028643 — `rewrite`
- intisari-v4-029244 — `discard`
- intisari-v4-029540 — `rewrite`
- intisari-v4-029571 — `keep_light_edit`
- intisari-v4-030502 — `rewrite`
- intisari-v4-032430 — `keep_light_edit`
- intisari-v4-032673 — `rewrite`
- intisari-v4-033744 — `rewrite`
- intisari-v4-034448 — `rewrite`
- intisari-v4-034729 — `rewrite`
- intisari-v4-034913 — `discard`
