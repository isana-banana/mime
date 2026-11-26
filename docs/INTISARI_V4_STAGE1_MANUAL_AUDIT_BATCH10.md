# Audit Manual Tahap 1 — Batch 10 (100 ID)

Branch: `experiment/intisari-v4-curation`

- Baris yang diperiksa: 100
- ID baru dan unik: 100
- Dipertahankan untuk tahap berikutnya: 37
- Dikeluarkan karena topik digital: 63
- ID duplikat: 0
- Status training: belum disetujui (`training_ready=false`)

## Pedoman keputusan

Penyaringan ini melihat pokok percakapan, bukan sekadar kata yang muncul. Percakapan tentang resep dan memasak tetap dipertahankan meskipun menyebut internet atau YouTube. Begitu juga latihan futsal/badminton, perjalanan KRL, kegiatan kampus, rapat kerja, dan belanja langsung di pasar atau mal tetap dipertahankan bila konteks luringnya jelas.

Sebaliknya, percakapan yang pokoknya membahas gim digital, media sosial, Wi-Fi, email, perangkat komputer/HP, aplikasi, atau toko daring dikeluarkan. Percakapan belanja yang masih memiliki konteks nyata di mal atau pasar dipertahankan untuk pemeriksaan mutu berikutnya; penyebutan aplikasi tidak otomatis membuatnya gugur.

Percakapan yang dipertahankan belum tentu bermutu. Kesalahan bahasa, pengulangan, alur yang rusak, dan ketepatan jawaban akan diperiksa pada tahap 3. Kata ganti seperti gue/lo juga belum disunting pada tahap ini.

## Hasil

| Keputusan | Jumlah |
|---|---:|
| `keep_in_scope` | 37 |
| `exclude_digital_topic` | 63 |
| Total | 100 |

Keputusan ini hanya menyaring topik. Data yang dipertahankan belum otomatis layak untuk training dan tetap harus melalui tahap penyeragaman kata ganti serta pemeriksaan mutu.
