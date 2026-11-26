# Ringkasan konsolidasi audit ulang persona — INTISARI V4

## Cakupan yang sudah diperiksa ulang

| Kelompok | ID unik |
|---|---:|
| Audit ulang tahap 3 berdasarkan dialog lengkap | 52 |
| Audit ulang terarah dari sampel tahap 2 | 33 |
| **Total unik yang diperiksa ulang** | **85** |

Audit tahap 3 mencakup 45 dialog pada batch utama dan 7 dialog tambahan. Label lama dari 41 catatan persona sebelumnya dibandingkan dan dikoreksi; catatan yang tumpang tindih tidak dihitung dua kali.

## Keputusan terbaru untuk 85 ID

| Keputusan | Jumlah |
|---|---:|
| Pertahankan dengan sunting ringan | 36 |
| Tulis ulang | 38 |
| Buang | 10 |
| Buang karena struktur | 1 |
| **Total** | **85** |

## Interpretasi
- **36** percakapan dapat dipertahankan setelah perapian bahasa.
- **38** masih memiliki inti percakapan yang berguna, tetapi perlu ditulis ulang.
- **10** memang tidak layak dipakai karena makna rusak, jawaban tidak relevan, atau informasi yang tidak dapat dipastikan.
- **1** dibuang karena label pembicara tertanam dan struktur percakapan rusak.

Cerita asisten tentang tubuh, pekerjaan, keluarga, teman, hewan, makanan, selera, rutinitas, olahraga, perjalanan, dan pengalaman pribadi tidak lagi menjadi alasan penolakan tersendiri.

## Berkas rincian
- `docs/INTISARI_V4_PERSONA_POLICY.md`
- `docs/INTISARI_V4_PERSONA_REAUDIT_BATCH1.md`
- `docs/INTISARI_V4_PERSONA_REAUDIT_BATCH2.md`
- `docs/INTISARI_V4_PERSONA_REAUDIT_BATCH3.md`
- `docs/INTISARI_V4_PERSONA_REAUDIT_STAGE3_ADDENDUM.md`
- `docs/INTISARI_V4_STAGE2_PERSONA_REAUDIT.md`
- Data per ID tersedia dalam berkas JSONL berpasangan di `data/curated/intisari_v4/`.

## Yang belum selesai
- Audit ulang 198 contoh lain dari 250 audit tahap 3 belum dilakukan dengan pedoman baru.
- Audit ulang 67 contoh lain dari sampel tahap 2 belum dilakukan dengan pedoman baru.
- Sampel-sampel ini bukan pengganti audit penuh atas kumpulan 30.625 kandidat.
- Semua keputusan masih berstatus `training_ready: false`. Belum ada data yang disetujui untuk training.

## Aturan keputusan ke depan
Persona pribadi boleh. Yang dinilai adalah konsistensi cerita, relevansi jawaban, mutu bahasa, serta ketepatan informasi dunia nyata. Jangan mengarang fakta tentang pengguna; jangan menebak detail yang tidak ada di sumber saat menyunting.
