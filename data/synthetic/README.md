# Korpus sintetis MIME-ID

Folder ini berisi percakapan orisinal yang disusun oleh ChatGPT sebagai data kandidat, bukan data training yang otomatis dipercaya.

## Batch awal

- `seed_v1.jsonl`: 25 percakapan dalam bahasa Indonesia.
- Setiap baris adalah satu objek JSON dengan `id`, `topic`, `style`, dan `messages`.
- Pesan memakai role `user` dan `assistant` secara bergantian.
- Percakapan dibuat untuk konteks sehari-hari, jawaban sederhana, dan gaya bahasa yang beragam.

## Aturan pembuatan

1. Jangan membuat asisten mengaku punya tubuh, pekerjaan, keluarga, pengalaman pribadi, atau bisa melakukan tindakan di dunia nyata.
2. Jangan menciptakan harga, alamat, jadwal, nomor telepon, rute, atau fakta lokal spesifik.
3. Untuk topik kesehatan, hukum, keuangan, keselamatan, dan topik berisiko, jangan memberi instruksi ahli yang tidak didukung sumber. Batch dasar sebaiknya menghindari topik tersebut.
4. Jawaban harus menjawab pertanyaan, tidak mengarang konteks, tidak selalu membuka dengan frasa yang sama, dan tidak memaksa slang.
5. Seimbangkan ragam bahasa: aku/kamu, saya/Anda, dan gue/lo. Jangan jadikan satu ragam sebagai satu-satunya suara model.
6. Variasikan panjang jawaban, jumlah giliran, maksud pengguna, dan bentuk pertanyaan. Hindari mengganti nama benda pada template yang sama.
7. Jangan membuat ribuan contoh sekaligus tanpa audit. Buat batch kecil, periksa sampel acak, cari duplikasi, lalu perbaiki aturan.

## Gerbang penggunaan

Batch sintetis **tidak otomatis masuk ke training**. Ia harus:
- lolos pemeriksaan format, urutan role, duplikasi, dan aturan kualitas;
- diperiksa sampelnya secara manual;
- dibandingkan dengan data lain untuk menghindari gaya yang terlalu seragam;
- disetujui sebelum pipeline training menggunakannya.

Korpus sintetis juga punya risiko menyalin bias atau kesalahan guru AI. Banyak data tidak selalu berarti banyak pengetahuan baru. Tujuan batch ini adalah mengajarkan pola percakapan yang jelas dan natural, bukan mengklaim kebenaran faktual.
## Batch berikutnya

- `seed_v2.jsonl`: batch lanjutan 25 percakapan.
- `seed_v3.jsonl`: 50 percakapan, ID `syn0051`–`syn0100`.
- `seed_v4.jsonl`: 100 percakapan, ID `syn0101`–`syn0200`.
- Batch v4 sudah diperiksa untuk ID unik dan duplikasi kalimat pembuka; kapitalisasi awal kalimat pada ragam `saya/Anda` dan `gue/lo` juga dirapikan.
- Semua batch tetap berstatus kandidat dan memerlukan pemeriksaan manual sebelum dipakai untuk training.
- Pemeriksaan tambahan batch v4: satu jawaban pembuka yang berulang diganti agar variasi respons lebih baik.
