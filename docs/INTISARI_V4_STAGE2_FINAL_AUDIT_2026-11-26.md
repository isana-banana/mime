# Hasil Final Tahap 2 — Penyeragaman Kata Ganti

Branch: `experiment/intisari-v4-curation`

## Hasil pemrosesan

- Percakapan diproses: **45.717**
- Percakapan yang berubah: **24.783**
- Sisa `gue/gua/gw/lo/lu/elo/elu`: **0**
- Semua hasil tetap `training_ready=false`

## Penggantian

| Bentuk awal | Bentuk hasil | Jumlah |
|---|---|---:|
| gue | aku | 58.788 |
| gua | aku | 15 |
| gw | aku | 3 |
| lo | kamu | 7.361 |
| saya | aku | 7.176 |
| anda | kamu | 7 |

## Aturan register yang dipakai

- Jika percakapan sudah memakai gaya akrab seperti `aku/kamu` atau slang yang sedang dibersihkan, `saya` disesuaikan menjadi `aku` dan `Anda` menjadi `kamu` agar pasangan kata ganti konsisten.
- Jika percakapan memakai gaya formal `saya/Anda` tanpa tanda gaya akrab, bentuk formal dipertahankan.
- Huruf kapital di awal kata tetap dijaga.
- Kata ganti lain dan isi percakapan tidak diubah oleh tahap ini.

Uji otomatis mencakup penggantian slang, pelestarian pasangan formal, dan penyesuaian `saya/Anda` hanya dalam dialog akrab. Semua uji lulus pada workflow GitHub Actions.

## Tahap 3 — pemindaian mutu mekanis

Tahap 3 dijalankan pada hasil final Tahap 2:

- Total dipindai: **45.717**
- Perlu pemeriksaan manusia: **8.460**
- Tidak ada masalah mekanis yang terdeteksi: **37.257**

Tidak adanya tanda mekanis bukan persetujuan mutu. Seluruh 45.717 percakapan tetap perlu pemeriksaan makna, relevansi, kewajaran, konsistensi, dan ketepatan fakta. Belum ada data yang disetujui untuk training.

Workflow berhasil: https://github.com/isana-banana/mime/actions/runs/45834094573
