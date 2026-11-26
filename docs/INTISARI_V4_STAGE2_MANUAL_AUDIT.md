# INTISARI V4 — audit manual tahap 2

## Ruang lingkup
Audit ini menilai **100 percakapan secara manual** dari berkas `candidate_unreviewed.jsonl`, yaitu keluaran yang sudah lolos penyaringan mekanis tahap 1. Sampel diambil secara acak dengan dua seed yang dicatat di lembar kerja. Ini adalah pemeriksaan sampel, bukan pemeriksaan penuh terhadap 31.497 calon.

## Hasil penilaian sampel

| Keputusan | Jumlah | Arti |
|---|---:|---|
| Pertahankan dengan sunting ringan | 21 | Inti dialog cukup baik, masih perlu perapian |
| Tulis ulang | 26 | Topik masih berguna, tetapi jawaban/kalimat perlu diperbaiki |
| Buang | 43 | Makna rusak, jawaban tidak nyambung, atau mutu terlalu rendah |
| Keluarkan karena topik | 5 | Membahas akun/media sosial, kabel/koneksi, atau komputasi |
| Buang karena struktur | 5 | Label pembicara tertanam, konteks hilang, atau placeholder |
| **Total** | **100** | |

**Makna hasil:** hanya 21% sampel yang cukup baik untuk dipertahankan dengan suntingan ringan. Sebanyak 26% masih mungkin diselamatkan dengan penulisan ulang. Angka ini menggambarkan sampel 100, bukan estimasi pasti untuk seluruh dataset.

## Pola masalah yang ditemukan
1. **Jawaban tidak menjawab pertanyaan** — misalnya pertanyaan makan siang dibalas dengan informasi hujan.
2. **Kalimat rusak** — kata salah bentuk, susunan kata tidak wajar, atau makna tidak dapat dipastikan.
3. **Percakapan berputar** — mengulang pertanyaan atau jawaban tanpa menambah isi.
4. **Jawaban terlalu umum** — benar secara bentuk, tetapi tidak membantu.
5. **Klaim faktual tanpa dasar atau keliru** — terutama saat memberi informasi nyata seperti harga, cuaca, waktu perjalanan, atau saran.
6. **Label pembicara masuk ke isi** — misalnya `Aku:` dan `Kamu:` ditulis sebagai bagian pesan.
7. **Konteks tidak lengkap** — pesan seperti “Kenapa?” tidak dapat dinilai tanpa percakapan sebelumnya.

## Aturan persona asisten (berlaku untuk audit ulang dan batch berikutnya)
- Asisten boleh memiliki tubuh, pekerjaan, keluarga, teman, hewan peliharaan, rumah, kendaraan, kesukaan, kebiasaan, dan pengalaman pribadi sebagai bagian dari persona percakapan.
- Jangan memberi label buruk atau membuang dialog hanya karena asisten bercerita “aku lapar”, “aku punya kucing”, “aku bekerja”, atau “aku pernah pergi”.
- Yang perlu diperiksa adalah apakah cerita itu relevan, masuk akal, dan konsisten di dalam dialog. Kontradiksi nyata, perubahan cerita tanpa alasan, atau jawaban yang menghindari pertanyaan tetap perlu diperbaiki.
- Bedakan cerita persona (dinilai dari kelancaran dan konsistensi internal) dengan informasi dunia nyata atau nasihat (dinilai dari ketepatan faktanya).
- Saat menyunting, jangan menambah pengalaman, keluarga, tempat, angka, atau kejadian baru yang tidak didukung sumber. Pertahankan detail persona yang sudah ada jika dialognya baik.

## Keputusan penyuntingan
- Jangan mengubah kata secara global jika dapat mengubah maksud.
- Pertahankan inti yang benar; jangan menambah fakta atau alasan yang tidak ada di sumber.
- Jika jawaban sumber salah atau tidak nyambung, tulis ulang dengan jawaban yang relevan atau buang.
- Gunakan `aku-kamu` untuk percakapan akrab dan `saya-Anda` untuk percakapan sopan; konsisten dalam satu dialog.
- Topik pasar, makanan, kebun, keluarga, sekolah, pekerjaan, dan perjalanan tetap dapat dipakai. Jangan mengeluarkan topik hanya karena menyebut toko atau tempat umum; yang dikeluarkan adalah topik digital/perangkat yang memang tidak sesuai fokus.

## Pilot penyuntingan
File `data/curated/intisari_v4/pilot_edited_10.jsonl` memuat 10 contoh hasil suntingan awal. Semua diberi status `pilot_edited_not_training_ready`; contoh tersebut belum boleh dicampur ke dataset pelatihan sebelum ditinjau kembali.

## Catatan penilaian ulang
Label audit tahap 2 dibuat dengan pedoman lama. Jika alasan buang/tulis ulang hanya karena asisten mengaku memiliki tubuh, pekerjaan, keluarga, hewan, atau pengalaman, label tersebut wajib ditinjau ulang. Jangan mengubah keputusan tanpa membaca dialog lengkap dan memeriksa mutu lainnya.

## Kesimpulan
Penyaringan mekanis tahap 1 terlalu longgar untuk dijadikan penentu mutu. Calon tidak boleh disebut data bersih. Tahap selanjutnya harus menggabungkan aturan mekanis dengan audit semantik bertahap.

**Training tetap dinonaktifkan.** Tidak ada data dari tahap ini yang dinyatakan siap latih.
