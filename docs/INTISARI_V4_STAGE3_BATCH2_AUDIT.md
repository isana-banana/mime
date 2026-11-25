# INTISARI V4 — audit manual tahap 3, batch 2 (50 percakapan)

## Ruang lingkup
Sampel acak baru berisi 50 percakapan dari kumpulan 30.625 calon. ID yang sudah dinilai pada audit 100 sebelumnya dan batch 1 dikeluarkan. Satu ID yang ternyata bertumpang tindih saat pemeriksaan silang diganti dengan sampel baru. Seed: `20261128`. Data mentah tidak diubah.

## Hasil

| Keputusan | Jumlah | Persentase |
|---|---:|---:|
| Pertahankan dengan sunting ringan | 3 | 6% |
| Tulis ulang | 20 | 40% |
| Buang | 27 | 54% |
| Keluarkan karena topik | 0 | 0% |
| **Total** | **50** | **100%** |

## Pola masalah
- Asisten mengaku lapar, makan, bepergian, punya hewan, punya resep, atau dapat hadir secara fisik.
- Banyak jawaban hanya mengulang pengguna atau tidak menjawab pertanyaan.
- Ada klaim rute perjalanan, harga, keadaan cuaca, dan pengalaman pribadi tanpa dasar.
- Resep dengan takaran yang rusak harus dibuang, bukan diperhalus begitu saja.
- Toko fisik, supermarket, makanan, kebersihan, dan kegiatan sehari-hari tetap termasuk topik yang boleh dipakai bila isinya baik.

## Catatan batas topik
Tidak ada contoh yang perlu dikeluarkan khusus karena topik pada batch ini. Ini tidak berarti penyaringan topik sudah sempurna; sampel ini hanya kebetulan tidak menemukan contoh digital yang jelas.

## Status
Semua contoh tetap belum siap latih. `keep_light_edit` dan `rewrite` adalah calon untuk penyuntingan, bukan persetujuan masuk korpus. Training tetap dinonaktifkan.

Rincian ID dan alasan ada di `data/curated/intisari_v4/manual_audit_batch2_50.jsonl`.
