# INTISARI V4 — audit ulang persona berdasarkan dialog lengkap (45 contoh)

## Metode
45 contoh dipilih dari catatan audit tahap 3 yang sebelumnya secara eksplisit menyebut kehidupan pribadi, pengalaman, tubuh, pekerjaan, kepemilikan, selera, atau kemampuan asisten sebagai alasan penilaian. Dialog lengkap diperiksa kembali dari kumpulan calon hasil kurasi. Penilaian baru mengikuti `INTISARI_V4_PERSONA_POLICY.md`.

## Hasil
| Keputusan baru | Jumlah |
|---|---:|
| Pertahankan dengan sunting ringan | 20 |
| Tulis ulang | 16 |
| Buang | 8 |
| Buang karena struktur | 1 |
| **Total** | **45** |

## Temuan
- Cerita tentang pekerjaan, teman, kucing, anjing, makan, selera, buku, musik, olahraga, perjalanan, dan hadir secara fisik tidak otomatis ditolak.
- Sejumlah keputusan lama berubah setelah dialog lengkap dibaca. Contohnya, pengalaman makan siang, bekerja, memiliki buku, bermain badminton, dan mengajak bertemu dapat dipertahankan setelah perapian.
- Contoh tetap ditulis ulang atau dibuang jika ada kontradiksi, salah mengambil sudut pandang, jawaban tidak relevan, fakta pengguna dikarang, atau bahasa rusak.
- Satu contoh tetap dibuang karena label pembicara tertanam dan struktur dialog rusak.

## Berkas rincian
`data/curated/intisari_v4/persona_reaudit_batch3_45.jsonl` memuat keputusan per ID. Berkas audit lama tidak dihapus; batch ini menjadi koreksi terbaru untuk contoh-contoh tersebut.

## Batas
Audit ini mencakup 45 contoh yang terpilih karena alasan persona tampak jelas pada label awal. Ini belum merupakan audit ulang seluruh 250 contoh tahap 3 atau 100 contoh tahap 2. Semua data tetap `training_ready: false`; training belum diizinkan.
