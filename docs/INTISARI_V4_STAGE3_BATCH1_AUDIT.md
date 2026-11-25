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

Hanya 2 contoh cukup baik dengan perbaikan kecil. Hasil ini hanya berlaku untuk batch ini, bukan angka pasti seluruh 30.625 calon.

## Masalah utama
1. Asisten mengarang kehidupan pribadi: uang, buku, teman, kesukaan, atau pengalaman bepergian.
2. Jawaban tidak menjawab pertanyaan, berpindah topik, atau hanya mengulang kata pengguna.
3. Bahasa rusak: kata salah, susunan kalimat kacau, dan pesan terpotong.
4. Mengarang fakta: nama orang, tempat, acara, jumlah uang, atau informasi perjalanan.
5. Konteks tidak cukup untuk memahami pertanyaan.
6. Saran tidak membantu dan memakai sudut pandang yang salah.

## Batas topik
- Hotspot, akun, dan sinyal/koneksi termasuk topik digital dan dikeluarkan.
- Makanan khas Bali, pasar, warung, perjalanan, hewan, keluarga, dan kegiatan sehari-hari tetap boleh dipakai bila dialognya masuk akal.
- Pertemuan kerja biasa tidak otomatis dianggap topik digital.

## Tindak lanjut
- Label `keep_light_edit` dan `rewrite` belum berarti siap latih.
- Batch berikutnya harus memakai ID baru dan menyimpan seed, keputusan, serta alasan.
- Audit dilanjutkan bertahap; training tetap dinonaktifkan sampai audit semantik dan persetujuan selesai.
