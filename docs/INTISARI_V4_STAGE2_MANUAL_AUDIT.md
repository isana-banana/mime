# INTISARI V4 — audit manual tahap 2

## Ruang lingkup
Audit ini menilai **100 percakapan secara manual** dari berkas `candidate_unreviewed.jsonl`, yaitu keluaran yang sudah lolos penyaringan mekanis tahap 1. Sampel diambil secara acak dengan dua seed yang dicatat di lembar kerja. Ini adalah pemeriksaan sampel, bukan pemeriksaan penuh terhadap 31.497 calon.

## Hasil penilaian sampel

| Keputusan | Jumlah | Arti |
|---|---:|---|
| Pertahankan dengan sunting ringan | 21 | Inti dialog cukup baik, masih perlu perapian |
| Tulis ulang | 26 | Topik masih berguna, tetapi jawaban/kalimat perlu diperbaiki |
| Buang | 43 | Makna rusak, jawaban tidak nyambung, mengarang, atau mutu terlalu rendah |
| Keluarkan karena topik | 5 | Membahas akun/media sosial, kabel/koneksi, atau komputasi |
| Buang karena struktur | 5 | Label pembicara tertanam, konteks hilang, atau placeholder |
| **Total** | **100** | |

**Makna hasil:** hanya 21% sampel yang cukup baik untuk dipertahankan dengan suntingan ringan. Sebanyak 26% masih mungkin diselamatkan dengan penulisan ulang. Sebanyak 53% sebaiknya tidak masuk ke korpus hasil kurasi. Angka ini menggambarkan sampel 100, bukan estimasi pasti untuk seluruh dataset.

## Pola masalah yang ditemukan
1. **Jawaban tidak menjawab pertanyaan** — misalnya pertanyaan makan siang dibalas dengan informasi hujan.
2. **Asisten mengarang pengalaman atau kemampuan fisik** — misalnya menawarkan menjemput atau mengaku memiliki mobil/tempat tertentu.
3. **Kalimat rusak** — kata salah bentuk, susunan kata tidak wajar, atau makna tidak dapat dipastikan.
4. **Percakapan berputar** — mengulang pertanyaan atau jawaban tanpa menambah isi.
5. **Jawaban terlalu umum** — benar secara bentuk, tetapi tidak membantu.
6. **Klaim tanpa dasar** — seperti mengarang gaji pribadi, suhu, waktu perjalanan, atau rekomendasi tertentu.
7. **Label pembicara masuk ke isi** — misalnya `Aku:` dan `Kamu:` ditulis sebagai bagian pesan.
8. **Konteks tidak lengkap** — pesan seperti “Kenapa?” tidak dapat dinilai tanpa percakapan sebelumnya.

## Keputusan penyuntingan
- Jangan mengubah kata secara global jika dapat mengubah maksud.
- Pertahankan inti yang benar; jangan menambah fakta, pengalaman, tempat, angka, atau alasan yang tidak ada di sumber.
- Jika jawaban sumber salah atau tidak nyambung, jangan sekadar memperhalus tata bahasa: tulis ulang dengan jawaban yang relevan atau buang.
- Gunakan `aku-kamu` untuk percakapan akrab dan `saya-Anda` untuk percakapan sopan; konsisten dalam satu dialog.
- Hindari dialog yang membuat asisten seolah benar-benar memiliki tubuh, rumah, kendaraan, keluarga, atau pengalaman pribadi, kecuali konteksnya jelas merupakan permainan peran.
- Topik pasar, makanan, kebun, keluarga, sekolah, pekerjaan, dan perjalanan tetap dapat dipakai. Jangan mengeluarkan topik hanya karena menyebut toko atau tempat umum; yang dikeluarkan adalah topik digital/perangkat yang memang tidak sesuai fokus.

## Pilot penyuntingan
File `data/curated/intisari_v4/pilot_edited_10.jsonl` memuat 10 contoh hasil suntingan awal. Semua diberi status `pilot_edited_not_training_ready`; contoh tersebut belum boleh dicampur ke dataset pelatihan sebelum ditinjau kembali.

## Kesimpulan
Penyaringan mekanis tahap 1 terlalu longgar untuk dijadikan penentu mutu. 31.497 calon tidak boleh disebut data bersih. Tahap selanjutnya harus menggabungkan aturan mekanis dengan audit semantik bertahap. Sampel ini menunjukkan bahwa korpus sumber perlu diseleksi dengan ketat, bukan sekadar diperbaiki ejaannya.

**Training tetap dinonaktifkan.** Tidak ada data dari tahap ini yang dinyatakan siap latih.
