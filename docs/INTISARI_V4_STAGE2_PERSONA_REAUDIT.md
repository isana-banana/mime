# INTISARI V4 — audit ulang persona pada sampel tahap 2 (33 contoh)

## Ruang lingkup
Dari 100 contoh yang pernah dinilai pada tahap 2, dipilih 33 dialog yang isi lengkapnya menunjukkan cerita tubuh, pekerjaan, pengalaman, kepemilikan, selera, kegiatan fisik, atau kehidupan pribadi asisten. Semua dialog diperiksa kembali dari `candidate_unreviewed.jsonl` menggunakan pedoman persona terbaru.

## Hasil keputusan baru
| Keputusan | Jumlah |
|---|---:|
| Pertahankan dengan sunting ringan | 15 |
| Tulis ulang | 17 |
| Buang | 1 |
| **Total** | **33** |

## Prinsip koreksi
- Pengalaman membeli barang, makan, bekerja, menonton film, berolahraga, mengunjungi keluarga, membawa kamera, memiliki teman, serta mengajak bertemu tidak dianggap cacat dengan sendirinya.
- Contoh yang sebelumnya dinilai buruk dapat dipertahankan bila alur dan jawabannya masih masuk akal.
- Tulis ulang tetap diperlukan bila jawaban salah sudut pandang, tidak membantu, memberi fakta yang tidak berdasar, atau bahasanya rusak.
- Buang hanya bila makna tidak dapat dipulihkan atau percakapan memang tidak layak.

## Rincian
Keputusan per ID disimpan di `data/curated/intisari_v4/stage2_persona_reaudit_33.jsonl`. Indeks 100 contoh dan label lama tetap dipertahankan sebagai jejak audit. Berkas ini menjadi koreksi terbaru untuk 33 contoh yang diperiksa.

## Batas
Ini adalah audit ulang terarah, bukan audit ulang seluruh 100 contoh. Sisa 67 contoh belum diperiksa ulang dengan pedoman persona terbaru. Semua tetap `training_ready: false`; training tetap dinonaktifkan.
