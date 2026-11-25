# INTISARI V4 — kemajuan audit semantik bertahap

## Cakupan yang sudah diperiksa
Audit tahap 2 sebelumnya memeriksa 100 contoh. Audit tahap 3 kini memeriksa **150 contoh baru** dalam tiga batch acak berisi 50 percakapan. Pemeriksaan silang memastikan ID tahap 3 tidak bertumpang tindih dengan audit tahap 2 atau antarbatch tahap 3.

## Hasil gabungan tahap 3 (150 ID baru)

| Keputusan | Jumlah | Persentase |
|---|---:|---:|
| Pertahankan dengan sunting ringan | 11 | 7,3% |
| Tulis ulang | 56 | 37,3% |
| Buang | 79 | 52,7% |
| Keluarkan karena topik | 3 | 2,0% |
| Buang karena struktur | 1 | 0,7% |
| **Total** | **150** | **100%** |

Angka ini hanya hasil dari 150 sampel tahap 3, bukan taksiran pasti mutu seluruh kumpulan 30.625 calon.

## Temuan gabungan
- Masalah dominan: asisten mengarang pengalaman/kehidupan pribadi, jawaban tidak menjawab pertanyaan, pengulangan, kata atau susunan kalimat rusak, serta informasi yang keliru.
- Contoh yang membahas pasar, toko fisik, makanan, hewan, perjalanan, kuliah, pekerjaan, dan kegiatan sehari-hari tidak otomatis dikeluarkan. Mutu dialog tetap menjadi penentu.
- Topik digital yang jelas tetap dikeluarkan sesuai batas korpus.
- Informasi tempat, resep, transportasi, dan pengetahuan umum tidak boleh ditebak ketika sumber percakapan tidak mendukungnya.

## Langkah berikutnya
Lanjutkan batch acak 50 demi 50 sampai 500 contoh unik pada audit tahap 3. Sebelum menetapkan sampel baru, periksa ID terhadap audit tahap 2 dan seluruh batch tahap 3. Setelah 500 sampel, rangkum pola kesalahan, lalu lakukan penyuntingan terarah pada contoh yang layak.

**Training tetap dinonaktifkan.** Label `keep_light_edit` dan `rewrite` bukan persetujuan otomatis untuk masuk data latih.
