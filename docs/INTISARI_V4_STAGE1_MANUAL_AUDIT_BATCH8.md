# Audit Manual Tahap 1 — Batch 8

Branch: `experiment/intisari-v4-curation`

- Baris yang diperiksa: 25
- ID baru dan unik: 25
- Dipertahankan untuk tahap berikutnya: 12
- Dikeluarkan karena topik digital: 13
- ID duplikat: 0
- Status training: belum disetujui (`training_ready=false`)

## Catatan keputusan

Percakapan tentang memasak sambal goreng tetap dipertahankan meskipun internet disebut sebagai sumber resep. Begitu juga percakapan tentang film dan jadwal bioskop: situs web hanya menjadi alat untuk mencari jadwal, sedangkan pokoknya adalah film dan kegiatan menonton di bioskop. Percakapan tentang belanja langsung di pasar atau mal juga dipertahankan bila konteks fisiknya masih jelas.

Sebaliknya, dialog yang inti pembahasannya adalah gim digital, media sosial, pemrograman, atau toko daring dikeluarkan. Pada ID `000810`, konteks membeli barang di pasar masih nyata; pembahasan Wi-Fi dan tontonan digital dapat dipangkas kemudian pada tahap mutu.

## Hasil

| Keputusan | Jumlah |
|---|---:|
| `keep_in_scope` | 12 |
| `exclude_digital_topic` | 13 |
| Total | 25 |

Keputusan ini hanya menyaring topik. Data yang dipertahankan belum otomatis layak untuk training dan tetap harus melalui tahap penyeragaman kata ganti serta pemeriksaan mutu.
