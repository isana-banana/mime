# INTISARI V4 — kemajuan audit semantik bertahap

## Cakupan yang sudah diperiksa
Audit tahap 2 sebelumnya memeriksa 100 contoh. Audit tahap 3 menambahkan 100 contoh baru dalam dua batch acak, dengan pemeriksaan silang untuk mencegah ID bertumpang tindih dengan audit sebelumnya.

## Hasil audit tahap 3 (100 ID baru)

| Keputusan | Jumlah | Persentase |
|---|---:|---:|
| Pertahankan dengan sunting ringan | 5 | 5% |
| Tulis ulang | 36 | 36% |
| Buang | 57 | 57% |
| Keluarkan karena topik | 2 | 2% |
| **Total** | **100** | **100%** |

Hasil ini hanya menggambarkan 100 contoh yang diperiksa pada tahap 3. Jangan menganggapnya sebagai angka mutu pasti untuk seluruh kumpulan 30.625 calon.

## Temuan gabungan tahap 3
- Mutu bahasa dan kesinambungan dialog masih menjadi masalah besar.
- Pola paling sering: asisten mengarang pengalaman/kehidupan pribadi, jawaban tidak nyambung, pengulangan, kata rusak, dan klaim fakta tanpa dasar.
- Contoh yang menyebut pasar, toko fisik, makanan, hewan, perjalanan, atau kegiatan sehari-hari tidak otomatis dikeluarkan. Mutu dialog tetap menjadi penentu.
- Topik digital yang jelas tetap dikeluarkan sesuai batas korpus.

## Langkah berikutnya
Lanjutkan batch acak 50 demi 50 sampai 500 contoh unik pada audit tahap 3. Periksa tumpang tindih ID terhadap audit tahap 2 dan semua batch tahap 3 sebelum menetapkan sampel. Setelah itu, tinjau ulang kategori kesalahan dan lakukan penyuntingan terarah pada contoh yang layak.

**Training tetap dinonaktifkan.** Tidak ada contoh yang otomatis masuk data latih hanya karena diberi label `keep_light_edit` atau `rewrite`.
