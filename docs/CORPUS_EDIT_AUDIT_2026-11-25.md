# Laporan Penyuntingan Korpus Sintetis — Tahap 1

Tanggal: 25 November 2026  
Cabang: `experiment/mime-id-300k`

## Tujuan
Menyederhanakan kosakata dan mengarahkan korpus ke percakapan sehari-hari berbahasa Indonesia yang alami, tanpa pembahasan komputer dan teknologi digital.

## Hasil
- Jumlah awal: 553 percakapan.
- Dikeluarkan: 60 percakapan yang berpusat pada komputer, internet, aplikasi, perangkat digital, pengelolaan berkas digital, dan kegiatan daring.
- Dipertahankan setelah penyuntingan: 493 percakapan.
- Penggunaan gue/gua/lo/lu/elo/elu diubah ke aku/kamu; label gaya ikut disesuaikan.
- Percakapan yang hanya menyebut alat digital secara sampingan diubah agar tetap masuk akal dalam kehidupan luring, bukan otomatis dihapus.
- Kosakata yang terlalu resmi atau rumit diganti dengan kata yang lebih umum jika maknanya tetap terjaga.

## Berkas korpus
- `data/synthetic/seed_v1.jsonl` sampai `seed_v9.jsonl`
- Pedoman: `docs/SYNTHETIC_CORPUS_GUIDELINES.md`

## Hasil pemeriksaan otomatis
- 493 baris percakapan.
- 493 ID unik; tidak ada ID ganda.
- Tidak ada jawaban asisten yang sama persis.
- Tidak ditemukan gue/gua/lo/lu/elo/elu.
- Gaya percakapan hanya `casual_aku_kamu` dan `casual_saya_anda`.
- Tidak ada campuran aku/kamu dengan saya/Anda dalam satu percakapan.
- Susunan pesan dan peran user/assistant valid.
- Pemeriksaan kata kunci tidak menemukan sisa pembahasan komputer atau teknologi digital.

## Batas audit
Pemeriksaan otomatis di atas adalah pemeriksaan bentuk dan kata kunci. Ini belum membuktikan seluruh percakapan sudah alami, tidak berulang secara makna, atau selalu memberi jawaban terbaik. Perlu audit isi secara bertahap, terutama kewajaran bahasa, jawaban yang benar-benar menjawab, kesinambungan antarbalasan, keamanan, dan variasi topik.

## Keputusan
Korpus 493 percakapan ini menjadi dasar penyuntingan berikutnya. Belum dilakukan pelatihan ulang.
