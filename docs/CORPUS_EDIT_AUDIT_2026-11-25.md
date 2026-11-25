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


## Refini isi tahap ketiga — 25 November 2026

### Fokus pemeriksaan
Tahap ini meninjau tiga sisi isi: kewajaran bahasa sehari-hari, ketepatan jawaban terhadap giliran sebelumnya, dan variasi situasi serta cara menjawab. Pemeriksaan kemiripan kata dipakai untuk menemukan calon pengulangan, lalu setiap pasangan diperiksa dari isi percakapannya.

### Perubahan
- Dari 469 percakapan, 15 percakapan dihapus karena terlalu mirip dengan contoh lain atau masih berpusat pada daftar kontak/nomor anggota.
- Jumlah korpus sekarang 454 percakapan. Dari jumlah awal 553, total 99 percakapan telah dikeluarkan.
- Percakapan yang dipertahankan diperbaiki pada bagian yang terasa kaku, terlalu umum, berulang, atau kurang sesuai dengan kehidupan luring.
- Perbaikan khusus meliputi penggantian istilah "tenggat" menjadi "batas waktu", perbaikan salah tulis "di bekal" menjadi "di tas", penggantian rujukan dokumen digital menjadi kertas, dan penulisan ulang contoh percakapan tentang balasan pesan menjadi percakapan langsung.
- Topik jam alarm diubah menjadi jam beker; beberapa contoh rapat dan pembagian tugas diubah agar tidak bergantung pada pesan atau jalur komunikasi digital.
- Jawaban yang mengulang gagasan dalam satu percakapan diperbaiki, termasuk contoh memilih buku dan menyiapkan bekal.
- Beberapa saran diperjelas agar lebih berguna dan aman, khususnya penyimpanan bekal dan penanganan kertas berisi keterangan pribadi.

### Pengulangan yang ditangani
Pasangan dengan isi sangat mirip ditinjau, antara lain contoh pintu berderit, penyimpanan bahan di kulkas, daftar belanja, pembagian tugas rumah, sepatu basah, barang bawaan perjalanan, kursi belajar, kebiasaan membaca, portofolio, lampu meja, menu mingguan, tanaman menguning, dan belajar kelompok. Contoh yang lebih lemah dihapus; contoh yang masih memberi sudut pandang berbeda dipertahankan.

### Status pemeriksaan
Penyuntingan tahap ketiga telah diterapkan pada sembilan berkas korpus. Pemeriksaan struktur dan kata kunci setelah perubahan tetap perlu dijalankan sebelum korpus dipakai untuk training. Penilaian kemiripan otomatis hanya alat bantu; ia tidak membuktikan bahwa semua percakapan sudah unik atau alami.

Belum dilakukan pelatihan ulang.


## Pemeriksaan mutu akhir seluruh korpus — 25 November 2026

### Cakupan
Seluruh 454 percakapan yang ada sebelum pemeriksaan akhir dibaca berurutan, bukan hanya sampel. Pemeriksaan mencakup kewajaran bahasa, jawaban terhadap giliran sebelumnya, kesinambungan percakapan, keamanan saran, konsistensi kata ganti, topik digital yang mungkin tersisa, pengulangan, dan struktur JSONL.

### Perbaikan akhir
- Sejumlah kalimat yang masih kaku atau memakai istilah kurang sehari-hari disederhanakan.
- Rujukan yang berpotensi mengarah ke pesan digital atau kegiatan daring diubah menjadi percakapan langsung, catatan kertas, daftar tertulis, atau kegiatan luring yang masuk akal.
- Contoh permainan digital diubah menjadi permainan papan.
- Dua contoh yang sangat dekat tentang membaca peta dan menyusun foto di album dikeluarkan.
- Tiga contoh lain yang terlalu berulang tentang laci dapur/peralatan dapur dan variasi menu bekal dihapus.
- Saran tentang nasi sisa diperjelas: nasi perlu segera disimpan di lemari es setelah dingin; nasi yang terlalu lama dibiarkan di suhu ruang sebaiknya dibuang.
- Saran tentang kabel yang dimainkan kucing diperjelas agar kabel terlindung dan tidak dapat digigit atau ditarik.
- Satu label gaya percakapan diperbaiki agar sesuai dengan penggunaan saya–Anda.

### Jumlah akhir
- Sebelum pemeriksaan mutu akhir: 454 percakapan.
- Dihapus dalam pemeriksaan akhir: 5 percakapan yang berulang atau terlalu dekat.
- Jumlah akhir: **449 percakapan**.
- Jumlah awal: 553 percakapan; total yang dikeluarkan sepanjang seluruh tahap: **104 percakapan**.
- Berkas: seed_v1.jsonl sampai seed_v9.jsonl.

### Pemeriksaan otomatis setelah perbaikan
- 449 baris dan 449 ID unik; tidak ada ID ganda.
- Semua pesan memiliki urutan peran user/assistant yang benar dan isi tidak kosong.
- Semua label gaya dikenali; tidak ditemukan campuran aku–kamu dan saya–Anda dalam satu percakapan.
- Tidak ditemukan gue/gua/lo/lu/elo/elu.
- Tidak ditemukan kata kunci komputer atau layanan digital pada daftar pemeriksaan khusus.
- Tidak ditemukan istilah rumit yang masuk daftar pemeriksaan penyederhanaan tahap ini.
- Tidak ada jawaban asisten yang sama persis.
- Perbandingan kemiripan kata menemukan beberapa pasangan yang masih berdekatan, tetapi ditinjau manual dan dipertahankan karena situasi atau kebutuhan yang dibahas berbeda. Perbandingan kata bukan penilaian makna yang sempurna.

### Penilaian dan batasan
Pemeriksaan isi dilakukan pada seluruh percakapan yang ada pada saat audit, kemudian dilakukan perbaikan dan pemeriksaan ulang. Korpus sekarang lebih bersih dan lebih konsisten dengan sasaran bahasa sehari-hari luring. Namun, ini bukan jaminan bahwa setiap jawaban merupakan satu-satunya jawaban terbaik atau bahwa model yang dilatih darinya pasti lancar. Kualitas keluaran tetap harus diuji setelah training melalui percakapan baru yang tidak ada di korpus.

### Status
Korpus **lolos pemeriksaan editorial dan struktur dasar** untuk menjadi bahan uji training berikutnya. Ini bukan klaim bahwa mutu model sudah terbukti. Belum ada training yang dijalankan dalam tahap pemeriksaan ini.


## Audit mutu akhir menyeluruh — 25 November 2026

### Hasil pemeriksaan isi
Seluruh sembilan berkas JSONL dibaca ulang. Pemeriksaan mencakup kewajaran bahasa, kesinambungan jawaban, kecocokan dengan giliran sebelumnya, variasi situasi, pengulangan makna, dan keamanan saran sehari-hari.

### Perbaikan yang diterapkan
- 24 percakapan diperbaiki pada putaran akhir, lalu dua penyuntingan kecil tambahan dilakukan pada konsistensi kata ganti dan label topik.
- Petunjuk nasi sisa diperjelas: nasi matang yang dibiarkan lebih dari dua jam pada suhu ruang harus dibuang; untuk berikutnya simpan segera di lemari es. Jawaban tidak mengandalkan bau atau tampilan untuk menentukan keamanan.
- Percakapan kabel listrik dan kipas diperjelas agar tidak mendorong pembongkaran alat atau penggunaan kabel rusak.
- Pemeriksaan sepeda diperjelas, terutama bila bunyi berasal dari rem atau rem tidak pakem.
- Beberapa percakapan tentang menyiapkan bekal, mengatur acara, membagi tugas, dan mengumumkan kegiatan dibuat lebih jelas dan sesuai kehidupan luring.
- Label topik yang kurang tepat atau masih memakai istilah modern diganti dengan label yang lebih sederhana.
- Satu percakapan tentang nasi sisa yang terlalu mirip dengan contoh lain dihapus. Contoh lain tentang nasi sisa ditulis ulang agar fokus pada keamanan makanan, bukan mengulang resep.

### Jumlah korpus yang benar
Pengambilan ulang langsung dari branch menunjukkan jumlah sebelum audit akhir adalah 449 baris, bukan 454 seperti angka pada laporan tahap sebelumnya. Setelah satu contoh berulang dihapus, jumlah akhir adalah **448 percakapan**.

Jumlah per berkas:
- seed_v1.jsonl: 23
- seed_v2.jsonl: 22
- seed_v3.jsonl: 42
- seed_v4.jsonl: 85
- seed_v5.jsonl: 82
- seed_v6.jsonl: 39
- seed_v7.jsonl: 46
- seed_v8.jsonl: 70
- seed_v9.jsonl: 39

Ada ketidaksesuaian enam baris terhadap angka 454 yang pernah dilaporkan: lima baris sudah tidak ada saat pemeriksaan akhir dimulai, dan satu baris dihapus pada audit ini karena pengulangan isi. Riwayat penghapusan lima baris tersebut belum berhasil dipadankan dengan daftar penghapusan pada laporan lama. Karena itu, angka 448 dari berkas aktual dipakai sebagai patokan; catatan penghapusan historis perlu dianggap belum sepenuhnya direkonsiliasi.

### Pemeriksaan struktur dan kata kunci setelah perbaikan
- 448 baris dan 448 ID unik; tidak ada ID ganda.
- Susunan pesan dan label gaya valid.
- Tidak ada campuran aku–kamu dengan saya–Anda dalam satu percakapan.
- Tidak ditemukan gue/gua/lo/lu/elo/elu.
- Pemeriksaan kata kunci tidak menemukan istilah komputer atau teknologi digital dalam isi percakapan.
- Pemeriksaan daftar kosakata sulit yang ditetapkan tidak menemukan istilah sasaran.
- Tidak ada jawaban asisten yang sama persis, jawaban kosong, atau jawaban yang terlalu pendek menurut batas pemeriksaan.
- Pemeriksaan kemiripan kata setelah penghapusan contoh berulang tidak menemukan pasangan di atas ambang 0,34.

### Batas hasil
Pemeriksaan kemiripan kata tidak sama dengan penilaian makna oleh manusia dan tidak membuktikan seluruh contoh sempurna. Percakapan yang tersisa sudah ditinjau secara isi, tetapi tetap disarankan menjalankan evaluasi model terpisah setelah training. Training belum dijalankan.
