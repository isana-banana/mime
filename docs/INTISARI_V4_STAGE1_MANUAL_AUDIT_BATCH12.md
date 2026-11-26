# Audit Manual Tahap 1 — Batch 12 (Sisa 362 ID)

Branch: `experiment/intisari-v4-curation`

## Hasil

- ID baru diperiksa: **362**
- Dipertahankan dalam cakupan: **223**
- Dikeluarkan sebagai topik digital: **139**
- ID duplikat dari batch sebelumnya: **0**
- Semua catatan: `training_ready=false`

## Cakupan pemeriksaan

Batch terakhir ini menyatukan seluruh sisa antrean: 109 contoh campuran dan 253 contoh ambigu saja. Istilah seperti `kamera`, `layar`, dan `presentasi` tidak diputuskan hanya dari kata tersebut.

- Presentasi sekolah/kantor, rapat, tugas, perjalanan, makanan, olahraga, hiburan TV/film, keselamatan, dan kegiatan sehari-hari dipertahankan bila itu inti percakapannya.
- Percakapan tentang spesifikasi atau pembelian ponsel/kamera, jaringan, Zoom sebagai layanan, permainan digital, media sosial, video digital, serta belanja daring dikeluarkan bila itulah inti percakapan.
- Penyebutan kamera saat bepergian atau layar/TV sebagai hiburan tidak otomatis membuat percakapan dikeluarkan.
- Percakapan yang masih masuk cakupan tetapi bahasanya rusak atau tidak nyambung tetap akan dinilai pada Tahap 3, bukan dibuang hanya karena mutu bahasanya.

## Penutupan Tahap 1

- Antrean campuran: 1.427 dari 1.427 ID selesai diperiksa.
- Antrean ambigu saja: 253 dari 253 ID selesai diperiksa.
- Total audit manual: **1.680/1.680 ID unik (100%)**.
- Keputusan kumulatif: **588 dipertahankan**, **1.092 dikeluarkan**.
- Tidak ada sisa antrean manual Tahap 1.

Tahap 1 selesai, tetapi korpus belum siap untuk training. Tahap 2 harus dijalankan ulang pada daftar final hasil Tahap 1, lalu Tahap 3 harus menilai dan memperbaiki mutu percakapan.
