# INTISARI V4 — audit ulang sampel lama 100 (batch persona 2, 12 dialog)

## Ruang lingkup
12 dialog tambahan dari sampel manual tahap 2 dibaca ulang dengan aturan persona terbaru. Penilaian mempertimbangkan percakapan lengkap, bukan sekadar apakah asisten mengaku punya teman, kesukaan, rencana, atau pengalaman.

## Hasil keputusan baru

| Keputusan | Jumlah |
|---|---:|
| Pertahankan dengan sunting ringan | 2 |
| Tulis ulang | 6 |
| Buang | 4 |
| **Total** | **12** |

## Temuan
- Pilihan makan di warung, kesukaan suasana kafe, pengalaman merawat kucing, belanja di mal, memiliki teman, rencana bepergian, dan memiliki resep adalah detail persona yang diperbolehkan.
- Dialog tetap ditulis ulang atau dibuang bila kalimat rusak, alur tidak menjawab pertanyaan, resep tidak jelas, atau klaim cuaca nyata tidak punya konteks.
- Rencana bermain ski tidak ditolak karena asisten punya rencana pribadi, tetapi karena dialognya tidak masuk akal dalam konteks cuaca panas dan tidak dapat diperbaiki tanpa menebak.

## Rincian
Keputusan per ID tersimpan di `data/curated/intisari_v4/legacy100_persona_reaudit_batch2_12.jsonl`. Ini merupakan koreksi terpisah; label audit awal tetap disimpan.

## Batas
Bersama batch 1, sudah dibaca ulang 37 dari 100 dialog tahap 2. Semua hasil tetap `training_ready: false`. Training tetap dinonaktifkan.
