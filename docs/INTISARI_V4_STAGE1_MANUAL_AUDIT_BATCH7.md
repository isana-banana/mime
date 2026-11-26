# Audit Manual Tahap 1 — Batch 7

Branch: `experiment/intisari-v4-curation`

- Baris yang diperiksa: 25
- ID baru dan unik: 25
- Dipertahankan untuk tahap berikutnya: 9
- Dikeluarkan karena topik digital: 16
- ID duplikat: 0
- Status training: belum disetujui (`training_ready=false`)

## Catatan keputusan

Penyebutan toko daring oleh asisten tidak otomatis membuat percakapan tentang mal menjadi topik digital. Pada ID `000136`, `000138`, `000140`, `000142`, dan `000147`, pengguna jelas membicarakan belanja langsung atau promo di mal, sehingga percakapan dipertahankan untuk diperbaiki pada tahap mutu. Percakapan tentang cuaca juga dipertahankan meskipun aplikasi prakiraan disebut sekilas.

Sebaliknya, dialog yang inti pembahasannya adalah toko daring, media sosial, Wi-Fi/internet, atau gim digital dikeluarkan. Permintaan bantuan umum pada ID `000630` dipertahankan karena internet hanya disarankan oleh asisten, bukan menjadi topik yang diminta pengguna.

## Hasil

| Keputusan | Jumlah |
|---|---:|
| `keep_in_scope` | 9 |
| `exclude_digital_topic` | 16 |
| Total | 25 |

Semua keputusan ini hanya untuk penyaringan topik Tahap 1. Percakapan yang dipertahankan belum berarti sudah layak untuk training; tahap penyeragaman kata ganti dan pemeriksaan mutu tetap diperlukan.
