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
- `seed_v5.jsonl`: 100 percakapan, ID `syn0201`–`syn0300`.
- `seed_v6.jsonl`: 51 percakapan, ID `syn0301`–`syn0351`, dengan jumlah giliran yang lebih bervariasi dan percakapan lanjutan yang lebih panjang.
- `seed_v7.jsonl`: 60 percakapan, ID `syn0352`–`syn0411`.
- `seed_v8.jsonl`: 89 percakapan, ID `syn0412`–`syn0500`; batch ini melengkapi total 500 percakapan.
- `seed_v9.jsonl`: 53 percakapan, ID `syn0501`–`syn0553`; batch lanjutan berisi topik rumah, belajar, pekerjaan kelompok, hobi, dan pengelolaan kegiatan.
- Batch v4 sudah diperiksa untuk ID unik dan duplikasi kalimat pembuka; kapitalisasi awal kalimat pada ragam `saya/Anda` dan `gue/lo` juga dirapikan.
- Jumlah saat ini 553 percakapan (`syn0001`–`syn0553`). Semua batch tetap berstatus kandidat dan memerlukan pemeriksaan manual sebelum dipakai untuk training.
- Pemeriksaan tambahan batch v4: jawaban asisten yang berulang diperbaiki.
- Audit kini juga menandai jawaban asisten yang sama persis, memeriksa kecocokan gaya kata ganti, dan melaporkan variasi jumlah pesan.
- Pemeriksaan ulang batch v3 menemukan label gaya yang keliru pada `syn0068`–`syn0100`; labelnya sudah diperbaiki menjadi `casual_aku_kamu`.
- Sumber publik `LorthGyu/indonesian-chat` kini ditahan seluruhnya dari kandidat otomatis karena sampel yang lolos masih mengandung pengalaman pribadi palsu, kehadiran fisik palsu, dan klaim spesifik tanpa dasar. Data itu perlu ditinjau manusia sebelum dipakai.
