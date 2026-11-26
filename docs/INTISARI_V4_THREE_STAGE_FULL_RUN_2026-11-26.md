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

Audit manual atas 143 ID unik dari contoh campuran:
- 60 dipertahankan dalam cakupan.
- 83 dikeluarkan sebagai topik digital.
- Enam batch berisi 150 baris audit. Tujuh baris merupakan ID duplikat yang sudah tercatat pada batch sebelumnya; penghitungan kemajuan menggunakan ID unik.
- Masih ada 1.284 contoh campuran dan 253 contoh ambigu saja yang belum diperiksa, total 1.537 ID unik.


### Tahap 2 — Penyeragaman kata ganti

| Hasil | Jumlah |
|---|---:|
| Percakapan yang diproses | 46.809 |
| Percakapan yang berubah | 27.885 |
| Sisa variasi gue/gua/gw/lo/lu/elo/elu setelah penggantian | 0 |

Penggantian token:
- `gue` → `aku`: 61.121
- `gua` → `aku`: 17
- `gw` → `aku`: 3
- `lo` → `kamu`: 7.718
- Penyesuaian `saya` → `aku`: 12.484
- Penyesuaian `anda` → `kamu`: 259

Penyesuaian `saya/Anda` terjadi pada dialog yang memakai slang agar pasangan kata ganti tetap konsisten. Tahap 2 ini masih bersifat sementara sampai audit manual tahap 1 selesai; setelah itu hasilnya akan dijalankan ulang pada daftar yang sudah final.

### Tahap 3 — Pemeriksaan mutu mekanis

| Hasil | Jumlah |
|---|---:|
| Percakapan dengan tanda masalah mekanis | 8.735 |
| Tidak ada masalah mekanis yang terdeteksi | 38.074 |

Tanda masalah mencakup struktur giliran, kata berulang, placeholder, terlalu banyak giliran, kata rusak, pesan terlalu pendek, dan teks mencurigakan.

Tidak adanya tanda mekanis **bukan** bukti bahwa percakapan sudah bagus. Seluruh 46.809 contoh tetap membutuhkan pemeriksaan makna, relevansi, kewajaran, dan ketepatan fakta.

Audit mutu manual percontohan:
- 20 percakapan diperiksa.
- 13 ditulis ulang.
- 4 dibuang karena isi rusak berat.
- 3 dibuang karena struktur tidak dapat dipulihkan.

Audit mutu ini masih percontohan dan belum menjadi hasil akhir korpus.

## Status saat laporan dibuat

- Pemrosesan otomatis penuh selesai dan GitHub Actions berhasil.
- Tahap 1 masih perlu menyelesaikan audit manual antrean campuran.
- Tahap 2 sudah berjalan secara mekanis, tetapi akan diulang setelah keputusan tahap 1 final.
- Tahap 3 baru dimulai pada batch percontohan; pemeriksaan semantik menyeluruh belum selesai.
- Semua keluaran tetap `training_ready=false`. Belum ada data yang disetujui untuk training.
- Persona asisten yang memiliki keluarga, pekerjaan, hewan, tubuh, barang, rutinitas, selera, dan pengalaman pribadi tetap diperbolehkan.

Workflow: https://github.com/isana-banana/mime/actions/runs/45796983660
