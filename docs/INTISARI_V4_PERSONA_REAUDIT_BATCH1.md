# INTISARI V4 — audit ulang aturan persona (18 contoh)

## Tujuan
Audit ulang terbatas terhadap 18 contoh dari batch tahap 3 yang alasan awalnya secara jelas menyebut tubuh, pekerjaan, pengalaman, kesukaan, kebutuhan makan, teman, hewan, atau kemampuan fisik asisten. Pedoman baru menyatakan semua itu boleh sebagai bagian dari persona percakapan.

## Hasil audit ulang

| Keputusan baru | Jumlah |
|---|---:|
| Pertahankan dengan sunting ringan | 9 |
| Tulis ulang | 6 |
| Buang | 3 |
| **Total** | **18** |

## Perubahan penting
- Klaim pekerjaan, keluarga/teman, selera makan, rutinitas, hewan peliharaan, dan kemampuan fisik tidak lagi menjadi alasan penolakan.
- Sebagian contoh tetap perlu ditulis ulang atau dibuang karena masalah lain: jawaban tidak menjawab pertanyaan, sudut pandang tertukar, kalimat rusak, atau pengulangan tanpa makna.
- Contoh yang tetap dibuang bukan dibuang karena asisten memiliki kehidupan pribadi.

## Rincian
Keputusan dan alasan per ID tersimpan di `data/curated/intisari_v4/persona_reaudit_batch1_18.jsonl`. Berkas audit lama tidak dihapus; berkas ini menjadi koreksi terpisah dan harus dibaca bersama hasil batch asalnya.

## Batas
Ini baru 18 contoh terpilih yang alasan awalnya paling jelas terkait persona. Ini **bukan** audit ulang seluruh 250 contoh tahap 3 atau 100 contoh tahap 2. Semua keputusan tetap `training_ready: false`. Training tetap dinonaktifkan.
