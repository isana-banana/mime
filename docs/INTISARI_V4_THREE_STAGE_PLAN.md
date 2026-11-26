# INTISARI V4 — Alur kurasi tiga tahap

Branch: `experiment/intisari-v4-curation`

## Prinsip utama

File sumber `data/external/intisari_v4/intisari_v4.jsonl` tidak boleh diubah. Semua hasil dibuat sebagai artefak terpisah. Tahap berjalan berurutan dan tidak boleh melompati tahap.

## Tahap 1 — Relevansi topik

- Keluarkan percakapan yang jelas membahas internet, media sosial, aplikasi, akun digital, perangkat komputasi, layanan daring, game digital, pemrograman, atau topik komputasi.
- Percakapan belanja langsung di pasar, toko, supermarket, dan mal tetap masuk cakupan.
- Kata yang ambigu seperti presentasi, slide, kamera, layar, video, dan televisi tidak otomatis dibuang. Catat untuk pemeriksaan konteks.
- Hasil: `stage1_in_scope.jsonl`, `stage1_excluded_digital.jsonl`, `stage1_ambiguous_review.jsonl`.

## Tahap 2 — Bahasa dan kata ganti

- Cari variasi `gue/gua/gw` dan `lo/lu/elo/elu` pada seluruh percakapan yang lolos tahap 1.
- Ubah konsisten menjadi `aku/kamu`; pertahankan register percakapan selain kata ganti yang memang harus diselaraskan.
- Catat jumlah perubahan dan sisa kata slang yang belum tertangani.
- Hasil: `stage2_language_normalized.jsonl` dan laporan perubahan.

## Tahap 3 — Mutu percakapan

- Tandai masalah struktur, pesan kosong, placeholder, kata berulang, kata rusak yang dikenali, teks mencurigakan, percakapan terlalu panjang, dan pesan sangat pendek.
- Daftar tanpa masalah mekanis tetap wajib diperiksa secara semantik: jawaban harus nyambung, alami, relevan, konsisten, dan akurat untuk fakta dunia nyata.
- Perbaiki percakapan yang masih dapat diselamatkan. Hapus hanya jika makna rusak berat, konteks hilang, atau kesalahannya terlalu luas untuk diperbaiki tanpa mengarang.
- Persona asisten boleh memiliki tubuh, keluarga, pekerjaan, hewan, selera, barang, rutinitas, dan pengalaman pribadi. Jangan menghapusnya hanya karena itu.
- Hasil mekanis bukan persetujuan training. Seluruh hasil tetap `training_ready=false` sampai audit semantik selesai dan pengguna menyetujui.

## Catatan batas otomatisasi

Penyaringan topik dan pemeriksaan bentuk dapat dijalankan ke seluruh 50.047 baris secara konsisten. Penilaian relevansi yang ambigu dan mutu semantik tidak boleh diklaim selesai hanya dari pencocokan kata atau tes otomatis; keduanya memerlukan audit percakapan dalam batch yang dapat dilacak.
