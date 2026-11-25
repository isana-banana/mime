# INTISARI V4 — hasil audit penyaringan tahap 1

## Sumber dan integritas
- Sumber: `data/external/intisari_v4/intisari_v4.jsonl`
- Baris diproses: 50.047
- Baris JSON rusak: 0
- SHA-256 sumber: `eb25826bc0b932b8a8dd1f1d2995305bec1271f6c13aa0415b04cdfd99356589`
- Berkas mentah tidak diubah.

## Hasil penyaringan mekanis terbaru
- Calon belum ditinjau: 30.625
- Karantina: 19.422
- Pesan pengguna: 80.150
- Pesan asisten: 75.228
- Unit test aturan kurasi: lulus pada workflow terbaru.

Alasan yang paling sering terdeteksi:
- Topik digital/perangkat/permainan daring: 6.052
- Susunan giliran tidak benar: 5.412
- Susunan kalimat janggal: 3.405
- Jawaban mengulang pesan pengguna: 3.391
- Pengulangan kata: 1.851
- Placeholder dalam pesan: 1.409
- Percakapan terlalu panjang: 1.218
- Campuran ragam kata ganti: 878
- Kata rusak yang dikenali: 668
- Pesan terlalu pendek: 304
- Duplikat setelah normalisasi: 118
- Label pembicara tertanam di isi pesan: 88
- Pola teks mencurigakan: 73
- Teks terlalu panjang: 1

Satu percakapan dapat memiliki lebih dari satu alasan, jadi jumlah alasan tidak boleh dijumlahkan untuk memperoleh jumlah percakapan.

## Pemeriksaan manual
Audit manual tahap 2 memeriksa 100 percakapan acak dari kelompok calon. Hasil dan daftar ID ada di:
- `docs/INTISARI_V4_STAGE2_MANUAL_AUDIT.md`
- `data/curated/intisari_v4/manual_review_100_index.json`

Hasil sampel: 21 perlu sunting ringan, 26 perlu tulis ulang, 43 dibuang, 5 dikeluarkan karena topik, dan 5 dibuang karena struktur. Hasil ini hanya berlaku untuk sampel 100, bukan seluruh 30.625 calon.

## Kesimpulan mutu
**30.625 calon bukan 30.625 percakapan bersih.** Mereka hanya lolos pemeriksaan mekanis. Pemeriksaan berbasis aturan tidak dapat memastikan relevansi jawaban, kewajaran fakta, dan kesinambungan makna.

Penyaringan tambahan menambah deteksi istilah media sosial/komputasi serta placeholder seperti `...`. Hal ini mengurangi calon dari 31.497 menjadi 30.625. Perubahan tersebut memperbaiki cakupan pemeriksaan, tetapi tidak menyelesaikan masalah mutu semantik.

## Tahap kurasi berikutnya
1. Lanjutkan audit sampel acak bertahap agar cakupan penilaian makin luas.
2. Perbaiki otomatis hanya hal yang aman, seperti ejaan yang pasti dan konsistensi kata ganti.
3. Tulis ulang contoh hanya jika maksud dan alur percakapan masih jelas.
4. Buang contoh yang membutuhkan perubahan besar atau mengandung jawaban salah.
5. Lakukan audit ulang pada semua contoh yang telah disunting.

## Keputusan
- Berkas mentah tetap menjadi sumber yang tidak diubah.
- `candidate_unreviewed.jsonl` hanya antrean audit lanjutan.
- `quarantine.jsonl` berisi percakapan yang perlu ditinjau atau dibuang.
- Sepuluh contoh pilot di `data/curated/intisari_v4/pilot_edited_10.jsonl` masih berstatus `pilot_edited_not_training_ready`.
- Tidak ada keluaran yang dinyatakan siap latih.
- Training tetap dinonaktifkan sampai audit semantik selesai dan pengguna memberi persetujuan.
