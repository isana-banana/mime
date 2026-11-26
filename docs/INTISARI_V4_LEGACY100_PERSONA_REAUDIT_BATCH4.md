# Audit Ulang Persona Sampel Lama INTISARI V4 — Batch 4 (20 percakapan)

- Cabang: `experiment/intisari-v4-curation`
- Sumber: sampel manual 100 percakapan dari INTISARI V4.
- Cakupan batch ini: 20 ID yang belum masuk tiga batch audit ulang persona sebelumnya.
- Kebijakan: klaim persona asisten (tubuh, keluarga, pekerjaan, hewan, selera, dan pengalaman) diperbolehkan. Keputusan dibuat berdasarkan kejelasan, relevansi, kesinambungan, struktur, dan ketepatan isi.

## Hasil

| Keputusan | Jumlah |
|---|---:|
| `keep_light_edit` | 3 |
| `rewrite` | 14 |
| `discard` | 2 |
| `exclude_topic` | 0 |
| `discard_structure` | 1 |
| **Total** | **20** |

## Catatan penting

- Topik belanja langsung, kegiatan sehari-hari, dan pengalaman persona tidak dikecualikan hanya karena bukan topik digital.
- Jawaban tentang musim dan saran kesehatan/aktivitas perlu menghindari klaim mutlak yang tidak didukung konteks.
- Satu contoh ditandai `discard_structure` karena label pembicara tertanam dalam isi pesan dan peran menjadi rancu.
- Dua contoh dibuang karena makna atau konteksnya tidak dapat dipulihkan secara bertanggung jawab.
- Semua keputusan masih berstatus audit; `training_ready=false`. Tidak ada data yang otomatis disetujui untuk pelatihan.

## ID yang diperiksa

- intisari-v4-001732 — `rewrite`
- intisari-v4-002205 — `rewrite`
- intisari-v4-002798 — `rewrite`
- intisari-v4-004169 — `rewrite`
- intisari-v4-004891 — `rewrite`
- intisari-v4-005595 — `rewrite`
- intisari-v4-006265 — `keep_light_edit`
- intisari-v4-006667 — `rewrite`
- intisari-v4-006708 — `rewrite`
- intisari-v4-011712 — `discard`
- intisari-v4-012442 — `rewrite`
- intisari-v4-014323 — `rewrite`
- intisari-v4-014661 — `rewrite`
- intisari-v4-015055 — `keep_light_edit`
- intisari-v4-015216 — `rewrite`
- intisari-v4-016881 — `rewrite`
- intisari-v4-018773 — `discard`
- intisari-v4-018972 — `keep_light_edit`
- intisari-v4-019198 — `discard_structure`
- intisari-v4-020031 — `rewrite`
