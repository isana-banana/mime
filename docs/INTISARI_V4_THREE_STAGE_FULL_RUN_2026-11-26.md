# INTISARI V4 — Laporan Pemrosesan Tiga Tahap (26 November 2026)

Branch: `experiment/intisari-v4-curation`

## Sumber dan integritas

- Sumber: `data/external/intisari_v4/intisari_v4.jsonl`
- Baris diproses: 50.047
- JSON rusak: 0
- SHA-256 sumber: `eb25826bc0b932b8a8dd1f1d2995305bec1271f6c13aa0415b04cdfd99356589`
- File sumber tidak diubah.

## Hasil otomatis seluruh sumber

### Tahap 1 — Penyaringan topik

| Hasil | Jumlah |
|---|---:|
| Tetap dalam cakupan otomatis | 46.809 |
| Dikeluarkan sebagai topik digital yang jelas | 3.238 |
| Contoh campuran untuk pemeriksaan manual | 1.427 |
| Contoh dengan istilah ambigu, tetap dipertahankan | 346 |

Catatan: 1.427 contoh campuran dan 346 contoh ambigu dapat saling tumpang tindih. Contoh belanja di pasar, warung, supermarket, dan mal tidak otomatis dibuang karena menyebut internet, website, atau media sosial sekilas.

Audit manual atas 1.680 ID unik dari seluruh antrean manual Tahap 1:
- 588 dipertahankan dalam cakupan.
- 1.092 dikeluarkan sebagai topik digital.
- Dua belas batch berisi 1.687 baris audit. Tujuh baris merupakan ID duplikat dari batch sebelumnya; hasil dihitung berdasarkan 1.680 ID unik.
- Seluruh 1.427 contoh campuran dan 253 contoh ambigu saja sudah diperiksa. Tidak ada sisa antrean manual Tahap 1.


Rincian batch ketujuh: 25 ID baru diperiksa; 9 dipertahankan dan 16 dikeluarkan. Tidak ada ID duplikat pada batch ini. Laporan: `docs/INTISARI_V4_STAGE1_MANUAL_AUDIT_BATCH7.md`.

Rincian batch kedelapan: 25 ID baru diperiksa; 12 dipertahankan dan 13 dikeluarkan. Tidak ada ID duplikat pada batch ini. Laporan: `docs/INTISARI_V4_STAGE1_MANUAL_AUDIT_BATCH8.md`.

### Tahap 2 — Penyeragaman kata ganti

| Hasil | Jumlah |
|---|---:|
| Percakapan yang diproses | 45.717 |
| Percakapan yang berubah | 24.783 |
| Sisa variasi gue/gua/gw/lo/lu/elo/elu setelah penggantian | 0 |

Penggantian token:
- `gue` → `aku`: 58.788
- `gua` → `aku`: 15
- `gw` → `aku`: 3
- `lo` → `kamu`: 7.361
- Penyesuaian `saya` → `aku` pada dialog akrab: 7.176
- Penyesuaian `anda` → `kamu` pada dialog akrab: 7

Aturan register sudah diperbaiki: percakapan yang memakai gaya akrab (aku/kamu atau slang) diseragamkan ke pasangan `aku-kamu`; percakapan formal yang memakai `saya-Anda` tetap dipertahankan. Pemeriksaan akhir menunjukkan tidak ada sisa kata ganti slang yang ditargetkan. Tahap 2 mekanis selesai, tetapi sampel hasilnya tetap perlu diperiksa secara wajar saat audit mutu Tahap 3.

### Tahap 3 — Pemeriksaan mutu mekanis

| Hasil | Jumlah |
|---|---:|
| Percakapan dengan tanda masalah mekanis | 8.460 |
| Tidak ada masalah mekanis yang terdeteksi | 37.257 |

Tanda masalah mencakup struktur giliran, kata berulang, placeholder, terlalu banyak giliran, kata rusak, pesan terlalu pendek, dan teks mencurigakan.

Tidak adanya tanda mekanis **bukan** bukti bahwa percakapan sudah bagus. Seluruh 45.717 contoh tetap membutuhkan pemeriksaan makna, relevansi, kewajaran, dan ketepatan fakta.

Audit mutu manual percontohan:
- 20 percakapan diperiksa.
- 13 ditulis ulang.
- 4 dibuang karena isi rusak berat.
- 3 dibuang karena struktur tidak dapat dipulihkan.

Audit mutu ini masih percontohan dan belum menjadi hasil akhir korpus.

## Status saat laporan dibuat

- Pemrosesan otomatis penuh selesai dan GitHub Actions berhasil.
- Tahap 1 otomatis dan audit manual telah selesai; seluruh 1.680 ID unik sudah diputuskan.
- Tahap 2 sudah dijalankan ulang setelah keputusan manual Tahap 1 final; sisa slang target: 0.
- Pemindaian mekanis Tahap 3 selesai pada 45.717 percakapan; audit semantik manual menyeluruh masih belum selesai.
- Semua keluaran tetap `training_ready=false`. Belum ada data yang disetujui untuk training.
- Persona asisten yang memiliki keluarga, pekerjaan, hewan, tubuh, barang, rutinitas, selera, dan pengalaman pribadi tetap diperbolehkan.

Workflow: https://github.com/isana-banana/mime/actions/runs/45796983660

Rincian batch kesembilan: 25 ID baru diperiksa; 7 dipertahankan dan 18 dikeluarkan. Tidak ada ID duplikat pada batch ini. Laporan: `docs/INTISARI_V4_STAGE1_MANUAL_AUDIT_BATCH9.md`.

Rincian batch kesepuluh: 100 ID baru diperiksa; 37 dipertahankan dan 63 dikeluarkan. Tidak ada ID duplikat pada batch ini. Laporan: `docs/INTISARI_V4_STAGE1_MANUAL_AUDIT_BATCH10.md`.


## Perubahan ukuran batch audit manual

Mulai batch berikutnya, ukuran batch resmi ditetapkan menjadi **1.000 ID baru**. Agar pemeriksaan percakapan tetap teliti dan tidak hanya mengandalkan kata kunci, pelaksanaan dapat dibagi menjadi 10 subkelompok internal berisi 100 ID. Hasilnya baru dicatat sebagai satu batch 1.000 setelah semua percakapan diperiksa dan keputusan tiap ID selesai. ID yang belum diperiksa tidak dihitung sebagai kemajuan. Posisi terakhir setelah Batch 12 adalah 1.680 dari 1.680 ID unik; tidak ada sisa antrean manual. Semua keluaran tetap `training_ready=false`.


Rincian batch kesebelas: 1.000 ID baru diperiksa; 240 dipertahankan dan 760 dikeluarkan. Tidak ada ID duplikat. Laporan: `docs/INTISARI_V4_STAGE1_MANUAL_AUDIT_BATCH11.md`.

## Status terbaru setelah Batch 11

- Kemajuan audit manual Tahap 1: **1.318/1.680 ID unik (78,45%)**.
- Sisa: **362 ID unik**, terdiri dari 109 contoh campuran dan 253 contoh ambigu saja.
- Batch 12 telah memeriksa seluruh sisa 362 ID dan menutup audit manual Tahap 1.
- Keputusan kumulatif sementara: 365 dipertahankan dan 953 dikeluarkan.
- Seluruh data tetap `training_ready=false`.


Rincian batch kedua belas: 362 ID baru diperiksa; 223 dipertahankan dan 139 dikeluarkan. Tidak ada ID duplikat. Laporan: `docs/INTISARI_V4_STAGE1_MANUAL_AUDIT_BATCH12.md`.

## Status terbaru setelah Batch 12 — Tahap 1 selesai

- Audit manual Tahap 1: **1.680/1.680 ID unik (100%)**.
- Antrean campuran tersisa: **0**; antrean ambigu saja tersisa: **0**.
- Keputusan kumulatif: **588 dipertahankan** dan **1.092 dikeluarkan**.
- Tahap 2 telah dijalankan ulang pada daftar final hasil Tahap 1; tidak ada sisa gue/gua/gw/lo/lu/elo/elu.
- Tahap 3 sudah menandai 8.460 percakapan untuk pemeriksaan manusia; 37.257 lainnya tidak memiliki masalah mekanis yang terdeteksi, tetapi tetap belum disetujui secara makna.
- Seluruh keluaran tetap `training_ready=false`; belum ada data yang disetujui untuk training.
