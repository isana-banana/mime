# INTISARI V4 — audit ulang aturan persona (batch 2, 23 contoh)

## Tujuan
Audit ulang terhadap 23 contoh dari batch tahap 3 yang catatan awalnya menyebut kehidupan pribadi, pengalaman, kepemilikan, selera, atau kemampuan fisik asisten.

## Hasil

| Keputusan baru | Jumlah |
|---|---:|
| Pertahankan dengan sunting ringan | 8 |
| Tulis ulang | 9 |
| Buang | 6 |
| **Total** | **23** |

## Temuan
Cerita asisten tentang hewan, teman, perjalanan, makanan favorit, kebiasaan menghemat uang, buku, pekerjaan, rasa lapar/lelah, dan kegiatan bersama tidak ditolak hanya karena bersifat pribadi. Sebagian contoh tetap perlu diperbaiki karena salah mengambil sudut pandang, tidak menjawab pertanyaan, fakta dunia nyata kurang tepat, atau bahasa rusak.

## Rincian dan batas
Keputusan per ID ada di `data/curated/intisari_v4/persona_reaudit_batch2_23.jsonl`. Ini adalah koreksi terpisah untuk label lama, bukan penggantian diam-diam pada berkas audit asal.

Bersama batch 1, sudah ditinjau ulang 41 contoh terpilih. Ini belum mencakup seluruh 250 contoh tahap 3 atau 100 contoh tahap 2. Semua keputusan tetap `training_ready: false`; training tetap dinonaktifkan.
