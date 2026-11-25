# INTISARI V4 — hasil audit penyaringan tahap 1

## Sumber dan integritas
- Sumber: `data/external/intisari_v4/intisari_v4.jsonl`
- Baris diproses: 50.047
- Baris JSON rusak: 0
- SHA-256 sumber: `eb25826bc0b932b8a8dd1f1d2995305bec1271f6c13aa0415b04cdfd99356589`
- Berkas mentah tidak diubah.

## Hasil penyaringan mekanis terbaru
- Calon belum ditinjau: 31.497
- Karantina: 18.550
- Pesan pengguna: 80.150
- Pesan asisten: 75.228
- Unit test aturan kurasi: lulus.

Alasan yang paling sering terdeteksi:
- Topik digital/perangkat/permainan daring: 5.931
- Susunan giliran tidak benar: 5.412
- Susunan kalimat janggal: 3.405
- Jawaban mengulang pesan pengguna: 3.391
- Pengulangan kata: 1.851
- Percakapan terlalu panjang: 1.218
- Campuran ragam kata ganti: 878
- Kata rusak yang dikenali: 668
- Pesan terlalu pendek: 304
- Duplikat setelah normalisasi: 118
- Label pembicara tertanam di isi pesan: 88
- Pola teks mencurigakan: 73
- Teks terlalu panjang: 1

Satu percakapan dapat memiliki lebih dari satu alasan, jadi jumlah alasan tidak boleh dijumlahkan untuk memperoleh jumlah percakapan.

## Pemeriksaan manual sampel calon
Sampel acak 25 percakapan dari kelompok calon masih menunjukkan masalah semantik dan bahasa yang nyata:
- jawaban tidak menjawab pertanyaan atau mengarang konteks;
- kalimat tidak alami, misalnya susunan kata yang tidak masuk akal;
- kesalahan pilihan kata dan salah ketik yang tidak tercakup daftar kata rusak;
- jawaban resep atau penjelasan yang keliru;
- asisten mengulang jawaban atau memberi jawaban sangat umum;
- kata ganti sudah diseragamkan, tetapi sudut pandang pembicara masih tertukar;
- contoh dengan label `Aku:` / `Kamu:` yang seharusnya menjadi metadata, bukan isi percakapan.

Contoh masalah yang ditemukan pada sampel:
- pertanyaan tentang resep gudeg dijawab dengan bahan yang tidak sesuai;
- pertanyaan tentang cuaca dijawab dengan konteks yang tidak jelas;
- percakapan tidur berulang dengan jawaban yang tidak membantu;
- kalimat tentang makanan, taman, dan kegiatan yang memakai kata secara keliru.

## Kesimpulan mutu
**31.497 calon bukan 31.497 percakapan bersih.** Mereka hanya lolos pemeriksaan mekanis. Pemeriksaan berbasis aturan tidak dapat memastikan relevansi jawaban, kewajaran fakta, dan kesinambungan makna.

Dataset V4 memiliki banyak contoh yang tampak seperti percakapan, tetapi sebagian besar masih membutuhkan penilaian isi. Jangan menganggap seluruh calon layak dipakai hanya karena formatnya benar.

## Tahap kurasi berikutnya
1. Ambil sampel calon secara acak dan beri label manusia: layak, perlu sunting ringan, perlu tulis ulang, atau buang.
2. Susun daftar pola kesalahan berdasarkan sampel yang benar-benar dibaca.
3. Terapkan perbaikan otomatis hanya untuk hal yang aman, seperti kata ganti dan ejaan yang pasti.
4. Tulis ulang hanya contoh yang masih memiliki alur dan maksud yang bisa dipertahankan.
5. Buang contoh yang memerlukan perubahan besar atau mengandung jawaban salah.
6. Audit ulang seluruh keluaran dan bandingkan sampel sebelum/sesudah.

## Keputusan
- Berkas mentah tetap menjadi sumber yang tidak diubah.
- `candidate_unreviewed.jsonl` hanya antrean audit lanjutan.
- `quarantine.jsonl` berisi percakapan yang perlu ditinjau atau dibuang.
- Tidak ada keluaran yang dinyatakan siap latih.
- Training tetap dinonaktifkan sampai audit semantik selesai dan pengguna memberi persetujuan.
