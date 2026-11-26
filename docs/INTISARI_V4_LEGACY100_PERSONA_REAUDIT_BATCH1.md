# INTISARI V4 — audit ulang sampel lama 100 (batch persona 25)

## Ruang lingkup
Membaca ulang 25 dialog asli dari sampel manual tahap 2. Fokus batch ini adalah label lama yang berpotensi dipengaruhi anggapan bahwa asisten tidak boleh memiliki kehidupan pribadi. Setiap keputusan dibuat dari isi percakapan, bukan dari alasan ringkas pada indeks saja.

## Hasil keputusan baru

| Keputusan | Jumlah |
|---|---:|
| Pertahankan dengan sunting ringan | 9 |
| Tulis ulang | 16 |
| Buang | 0 |
| **Total** | **25** |

## Koreksi penting
- Pengalaman makan, selera makanan, hewan peliharaan, kegiatan olahraga, belanja, pekerjaan, gaji, rencana perjalanan, dan kebiasaan pribadi boleh dipertahankan sebagai persona.
- Contoh yang semula dibuang karena asisten mengaku menerima gaji, punya pengalaman menonton film, menawarkan tumpangan, atau punya rencana akhir pekan dinilai ulang. Beberapa tetap perlu ditulis ulang karena masalah relevansi, kalimat, atau sudut pandang, bukan karena persona.
- Dialog tentang promo di mal (ID `intisari-v4-000658`) dikembalikan ke cakupan topik. Belanja langsung di toko/mal bukan topik digital.
- Tidak ada contoh dalam batch ini yang harus dibuang hanya karena persona. Keputusan `rewrite` tetap diperlukan untuk memperbaiki mutu dialog.

## Rincian
Keputusan per ID dan alasan tersimpan di `data/curated/intisari_v4/legacy100_persona_reaudit_batch1_25.jsonl`. Label lama tetap disimpan sebagai jejak audit; berkas ini adalah koreksi terpisah.

## Batas
Ini baru 25 dari 100 contoh sampel tahap 2. Data tetap belum siap latih. Semua baris memiliki `training_ready: false`. Training tetap dinonaktifkan sampai seluruh audit dan penyuntingan selesai.
