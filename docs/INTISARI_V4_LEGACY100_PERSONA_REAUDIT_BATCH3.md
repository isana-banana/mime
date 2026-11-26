# INTISARI V4 — audit ulang sampel lama 100 (batch persona 3, 3 dialog)

## Ruang lingkup
Tiga ID dari sampel tahap 2 tidak lagi berada di `candidate_unreviewed.jsonl` pada artefak kurasi terbaru, sehingga diperiksa langsung dari `quarantine.jsonl`.

## Hasil

| Keputusan | Jumlah |
|---|---:|
| Tulis ulang | 3 |
| **Total** | **3** |

## Koreksi
- `intisari-v4-020311`: gaji tahunan dan tanggungan adalah detail persona yang boleh. Masalahnya salah ketik berat.
- `intisari-v4-019151`: jawaban tentang slide tidak menjawab pertanyaan dengan jelas.
- `intisari-v4-023128`: percakapan tugas kuliah dapat dipakai, tetapi pertanyaan tenggat berulang dan perlu dirapikan.

Ketiganya tidak dibuang karena asisten memiliki pekerjaan, gaji, atau kegiatan pribadi. Rincian per ID ada di `data/curated/intisari_v4/legacy100_persona_reaudit_batch3_3.jsonl`.

## Batas
Bersama dua batch sebelumnya, sudah dibaca ulang 40 dari 100 dialog tahap 2. Data tetap belum siap latih.
