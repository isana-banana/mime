# INTISARI V4 — audit manual tahap 3, batch 3 (50 percakapan)

## Ruang lingkup
- Sumber: `candidate_unreviewed.jsonl` dari artefak kurasi mekanis.
- Sampel: 50 percakapan acak, seed `20261129`.
- ID dari audit 100 sebelumnya serta batch 1 dan 2 tahap 3 dikecualikan.
- Pemeriksaan silang memastikan 50 ID batch ini unik terhadap 200 ID yang sudah dinilai.
- Data sumber tidak diubah.

## Hasil

| Keputusan | Jumlah | Persentase |
|---|---:|---:|
| Pertahankan dengan sunting ringan | 6 | 12% |
| Tulis ulang | 20 | 40% |
| Buang | 22 | 44% |
| Keluarkan karena topik | 1 | 2% |
| Buang karena struktur | 1 | 2% |
| **Total** | **50** | **100%** |

## Temuan utama
1. Jawaban sering mengulang pertanyaan, tidak memberi informasi yang diminta, atau menjawab dengan fakta yang keliru.
2. Kerusakan bahasa mencakup kata tidak bermakna, salah ketik berat, dan kalimat yang kehilangan hubungan makna.
3. Nama tempat, istilah transportasi, dan pengetahuan umum perlu diperiksa; jangan mempertahankan jawaban hanya karena terdengar lancar.
4. Dialog yang membahas resep, belanja di toko fisik, kuliah, pekerjaan, wisata, dan kegiatan harian tetap berada dalam cakupan topik.
5. Satu contoh permainan digital dikeluarkan sesuai batas topik. Satu contoh lain dibuang karena label pembicara tertanam di dalam isi pesan.
6. Catatan awal tentang asisten yang punya pekerjaan, kebiasaan, kesukaan, pengalaman wisata, atau kemampuan fisik **bukan alasan penolakan dengan sendirinya**. Periksa apakah persona konsisten, relevan, dan bahasanya baik.

## Catatan penyuntingan
- Contoh `keep_light_edit` masih harus melewati pemeriksaan ejaan, konsistensi sapaan, dan mutu akhir.
- Contoh `rewrite` harus ditulis ulang dengan menjaga maksud, termasuk detail persona yang memang ada dalam sumber.
- Jangan menambah pengalaman atau fakta dunia nyata saat memperbaiki dialog.
- Contoh resep atau informasi tempat yang tidak jelas tidak boleh diperbaiki dengan menebak.

## Status
Label batch ini dibuat dengan pedoman lama; contoh yang mungkin terpengaruh alasan persona harus ditinjau ulang. Semua 50 contoh tetap `training_ready: false`. Training tetap dinonaktifkan.

Rincian keputusan per ID tersimpan di `data/curated/intisari_v4/manual_audit_batch3_50.jsonl`.
