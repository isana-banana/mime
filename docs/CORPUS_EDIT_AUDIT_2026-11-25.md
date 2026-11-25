# Laporan Penyuntingan Korpus Sintetis — Tahap 1

Tanggal: 25 November 2026  
Cabang: `experiment/mime-id-300k`

## Tujuan
Menyederhanakan kosakata dan mengarahkan korpus ke percakapan sehari-hari berbahasa Indonesia yang alami, tanpa pembahasan komputer dan teknologi digital.

## Hasil
- Jumlah awal: 553 percakapan.
- Dikeluarkan: 60 percakapan yang berpusat pada komputer, internet, aplikasi, perangkat digital, pengelolaan berkas digital, dan kegiatan daring.
- Dipertahankan setelah penyuntingan: 493 percakapan.
- Penggunaan gue/gua/lo/lu/elo/elu diubah ke aku/kamu; label gaya ikut disesuaikan.
- Percakapan yang hanya menyebut alat digital secara sampingan diubah agar tetap masuk akal dalam kehidupan luring, bukan otomatis dihapus.
- Kosakata yang terlalu resmi atau rumit diganti dengan kata yang lebih umum jika maknanya tetap terjaga.

## Berkas korpus
- `data/synthetic/seed_v1.jsonl` sampai `seed_v9.jsonl`
- Pedoman: `docs/SYNTHETIC_CORPUS_GUIDELINES.md`

## Hasil pemeriksaan otomatis
- 493 baris percakapan.
- 493 ID unik; tidak ada ID ganda.
- Tidak ada jawaban asisten yang sama persis.
- Tidak ditemukan gue/gua/lo/lu/elo/elu.
- Gaya percakapan hanya `casual_aku_kamu` dan `casual_saya_anda`.
- Tidak ada campuran aku/kamu dengan saya/Anda dalam satu percakapan.
- Susunan pesan dan peran user/assistant valid.
- Pemeriksaan kata kunci tidak menemukan sisa pembahasan komputer atau teknologi digital.

## Batas audit
Pemeriksaan otomatis di atas adalah pemeriksaan bentuk dan kata kunci. Ini belum membuktikan seluruh percakapan sudah alami, tidak berulang secara makna, atau selalu memberi jawaban terbaik. Perlu audit isi secara bertahap, terutama kewajaran bahasa, jawaban yang benar-benar menjawab, kesinambungan antarbalasan, keamanan, dan variasi topik.

## Keputusan
Korpus 493 percakapan ini menjadi dasar penyuntingan berikutnya. Belum dilakukan pelatihan ulang.


## Audit isi lanjutan — 25 November 2026

### Hasil penyaringan kedua
- Dari 493 percakapan, 23 percakapan lain yang berpusat pada telepon, rekaman suara, kabel pengisi daya, pesan digital, pemberitahuan, berita dari akun daring, papan ketik, salindia, profil daring, kotak masuk, atau grup percakapan dihapus.
- Satu percakapan tentang salindia yang masih tertinggal juga dihapus.
- Total korpus sekarang 469 percakapan; dari jumlah awal 553, total 84 percakapan digital/kurang sesuai telah dikeluarkan.
- Percakapan umum yang dapat berlangsung secara luring disunting, bukan langsung dibuang. Contohnya daftar lagu ditulis di kertas, catatan ide memakai buku kecil, peta menggunakan peta lipat, dan jadwal memakai catatan biasa.

### Penyederhanaan bahasa tambahan
- Kata seperti kapasitas, tenggat, tindak lanjut, konfirmasi, rasio, gradasi, drainase, audiens, dan sumber daya diganti dengan ungkapan sehari-hari sesuai kalimat.
- Kalimat hasil penggantian otomatis yang terdengar janggal diperbaiki secara khusus.
- Satu percakapan tentang membuat prototipe diganti menjadi percakapan nyata tentang membuat tempat pensil dari kardus bekas.
- Label topik yang terlalu teknis atau tidak sesuai diperbaiki.

### Audit otomatis setelah penyuntingan
- 469 percakapan dengan 469 ID unik.
- Tidak ada ID ganda.
- Tidak ada jawaban asisten yang sama persis.
- Tidak ditemukan gue/gua/lo/lu/elo/elu.
- Tidak ada campuran aku-kamu dengan saya-Anda dalam satu percakapan.
- Semua susunan pesan dan label gaya valid.
- Pemeriksaan kata kunci tidak menemukan pembahasan komputer atau teknologi digital.

### Catatan mutu
Pemeriksaan isi dilakukan berurutan pada seluruh kelompok percakapan yang tersedia. Audit kemiripan jawaban memakai perbandingan kata sederhana tidak menemukan pasangan jawaban yang melewati ambang kemiripan 0,48; ini bukan bukti bahwa tidak ada pengulangan makna. Topik yang sering muncul, seperti menulis, belajar, belanja, bahasa, perjalanan, dan memasak, masih perlu dijaga variasi situasi serta bentuk jawabannya.

### Status
Belum dilakukan pelatihan ulang. Korpus 469 percakapan menjadi bahan untuk pemeriksaan mutu berikutnya, bukan tanda bahwa korpus sudah final.
