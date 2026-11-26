# INTISARI V4 — audit manual tahap 3, batch 1 (50 percakapan)

## Ruang lingkup
- Kumpulan calon saat pengambilan sampel: **30.625**.
- Sampel acak tanpa pengembalian: **50 percakapan**, seed `20261127`.
- Penilaian mencakup seluruh giliran yang tersedia. Data mentah tidak diubah.
- ID, keputusan, dan alasan per percakapan tersimpan di `data/curated/intisari_v4/manual_audit_batch1_50.jsonl`.

## Hasil

| Keputusan | Jumlah | Persentase |
|---|---:|---:|
| Pertahankan dengan sunting ringan | 2 | 4% |
| Tulis ulang | 16 | 32% |
| Buang | 30 | 60% |
| Keluarkan karena topik | 2 | 4% |
| **Total** | **50** | **100%** |

Hanya 2 contoh cukup baik dengan perbaikan kecil. Hasil ini hanya berlaku untuk batch ini, bukan angka pasti seluruh 30.625 calon. Label ini dicatat dengan pedoman audit saat itu dan belum otomatis disahkan sebagai label akhir.

## Masalah yang dicatat saat audit awal
- Jawaban tidak menjawab pertanyaan, berpindah topik, atau hanya mengulang kata pengguna.
- Bahasa rusak: kata salah, susunan kalimat kacau, dan pesan terpotong.
- Klaim fakta dunia nyata yang keliru atau tidak berdasar.
- Konteks tidak cukup untuk memahami pertanyaan.
- Saran tidak membantu dan memakai sudut pandang yang salah.
- Beberapa catatan awal menganggap cerita kehidupan pribadi asisten sebagai masalah. **Alasan ini tidak lagi berlaku dengan sendirinya** dan harus diperiksa ulang berdasarkan aturan persona terbaru.

## Batas topik
- Hotspot, akun, dan sinyal/koneksi termasuk topik digital dan dikeluarkan.
- Makanan khas Bali, pasar, warung, perjalanan, hewan, keluarga, dan kegiatan sehari-hari tetap boleh dipakai bila dialognya masuk akal.
- Pertemuan kerja biasa tidak otomatis dianggap topik digital.

## Tindak lanjut
- Audit ulang label yang mungkin dipengaruhi aturan persona lama sebelum menggabungkan hasil batch.
- Label `keep_light_edit` dan `rewrite` belum berarti siap latih.
- Training tetap dinonaktifkan sampai audit semantik dan persetujuan selesai.
