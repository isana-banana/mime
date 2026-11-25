# INTISARI V4 — hasil audit penyaringan tahap 1

## Sumber dan integritas
- Sumber: `data/external/intisari_v4/intisari_v4.jsonl`
- Baris diproses: 50.047
- Baris JSON rusak: 0
- SHA-256 sumber: `eb25826bc0b932b8a8dd1f1d2995305bec1271f6c13aa0415b04cdfd99356589`
- Berkas mentah tidak diubah.

## Hasil penyaringan mekanis
- Calon belum ditinjau: 31.546
- Karantina: 18.501
- Pesan pengguna: 80.150
- Pesan asisten: 75.228

Alasan yang paling sering terdeteksi:
- Topik digital: 5.931
- Susunan giliran tidak benar: 5.412
- Susunan kalimat janggal: 3.405
- Jawaban mengulang pesan pengguna: 3.391
- Pengulangan kata: 1.851
- Percakapan terlalu panjang: 1.218
- Campuran ragam kata ganti: 878
- Kata rusak yang dikenali: 668
- Pesan terlalu pendek: 304
- Duplikat setelah normalisasi: 118

Satu percakapan dapat memiliki lebih dari satu alasan, jadi jumlah alasan tidak boleh dijumlahkan untuk memperoleh jumlah percakapan.

## Pemeriksaan manual sampel
Sampel acak dari kelompok calon masih menunjukkan:
- jawaban yang tidak menjawab pertanyaan;
- kalimat yang terdengar tidak alami atau tidak masuk akal;
- kata yang salah atau berubah bentuk;
- jawaban resep atau penjelasan yang keliru;
- asisten kadang mengambil posisi seolah-olah melakukan kegiatan fisik bersama pengguna;
- kata ganti yang sudah dinormalisasi tetapi peran pembicara masih tertukar.

Artinya, pemeriksaan mekanis belum cukup untuk menetapkan kelayakan percakapan. Kelompok 31.546 adalah antrean untuk penilaian semantik, bukan korpus bersih dan bukan data siap latih.

## Keputusan
1. Pertahankan berkas mentah tanpa perubahan.
2. Gunakan `candidate_unreviewed.jsonl` hanya sebagai antrean audit lanjutan.
3. Gunakan `quarantine.jsonl` untuk pemeriksaan atau pembuangan berdasarkan alasan.
4. Perbaiki contoh yang masih dapat diselamatkan secara manual; buang contoh yang membutuhkan penulisan ulang besar.
5. Jangan jalankan training dari keluaran ini sampai audit semantik dan persetujuan pengguna selesai.
