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

## Pola masalah yang dicatat saat audit awal
- Jawaban mengulang pengguna atau tidak menjawab pertanyaan.
- Ada klaim rute perjalanan, harga, keadaan cuaca, dan informasi nyata yang perlu diperiksa ketepatannya.
- Resep dengan takaran yang rusak harus dibuang, bukan diperhalus begitu saja.
- Catatan lama juga menandai cerita persona seperti asisten lapar, makan, bepergian, punya hewan, resep, atau dapat hadir secara fisik. **Hal-hal ini diperbolehkan sebagai persona** dan bukan alasan buang tersendiri. Periksa relevansi dan konsistensinya di dalam dialog.

## Catatan batas topik
Tidak ada contoh yang perlu dikeluarkan khusus karena topik pada batch ini. Ini tidak berarti penyaringan topik sudah sempurna; sampel ini hanya kebetulan tidak menemukan contoh digital yang jelas.

## Status
Label batch ini dibuat dengan pedoman lama. Contoh yang mungkin dinilai buruk hanya karena persona asisten wajib ditinjau ulang sebelum keputusan dipakai sebagai label final. Semua contoh tetap belum siap latih. Training tetap dinonaktifkan.

Rincian ID dan alasan ada di `data/curated/intisari_v4/manual_audit_batch2_50.jsonl`.
