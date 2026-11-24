# MIME-ID 300K

Eksperimen model bahasa kecil berbahasa Indonesia. Cabang ini terpisah dari MIME-ID 100K dan tidak mengubah model 100K atau APK yang sudah ada.

## Rancangan model

- Tokenizer byte UTF-8: 256 byte + BOS + EOS = 258 token
- Panjang konteks: 128 token
- Lebar embedding: 96
- Transformer: 3 layer, 4 attention head
- Feed-forward: 256 unit
- Embedding token dan output memakai bobot bersama
- **298.656 parameter trainable**

`train.py` memeriksa jumlah parameter dan menghentikan training bila tidak tepat 298.656.

## Korpus Indonesia yang disederhanakan

Sumber korpus diganti ke `uonlp/CulturaX` dengan konfigurasi bahasa Indonesia `id`, yang berisi teks web alami dalam jumlah besar. Ini mengurangi ketergantungan pada teks cerita buatan/terjemahan yang sebelumnya terasa kaku. `prepare_data.py` membersihkan URL, HTML, karakter kontrol, dan format Markdown sederhana; memecah teks panjang menjadi potongan 15–90 kata; menyaring kalimat terlalu panjang, angka/simbol berlebihan, dan kata sangat panjang; memilih potongan pendek dengan kata-kata yang lebih umum dipakai sehari-hari, menolak banyak istilah panjang, campuran bahasa Inggris, pola dialog buatan, dan potongan yang tampak seperti judul/menu; serta menghapus duplikasi.

Fokusnya bahasa sehari-hari: rumah, keluarga, teman, sekolah, makanan, perjalanan, kegiatan, dan obrolan sederhana. Karena sumbernya teks web, masih ada kemungkinan teks formal, iklan, atau kalimat kurang alami ikut lolos. Workflow audit menyimpan 100 contoh acak untuk diperiksa sebelum hasilnya dipakai.

## Jalankan lokal

```bash
pip install -r requirements.txt
python prepare_data.py --dataset uonlp/CulturaX --config id --max-documents 50000
python train.py --data data/train.txt --steps 6000
python generate.py --checkpoint checkpoints/best.pt --prompt "Halo, apa kabar?"
```

## Training GitHub Actions

Buka tab **Actions**, pilih **Train MIME-ID 300K**, lalu **Run workflow**. Default: 6.000 langkah dan batch size 32. Setelah berhasil, unduh artefak `mime-id-300k-checkpoints` berisi `best.pt` dan `last.pt`. Workflow berjalan di CPU GitHub-hosted runner; waktu bergantung pada antrean dan beban runner, dengan batas waktu job 6 jam.

Model 300K tetap sangat kecil dibandingkan LLM modern. Peningkatan parameter dan korpus yang lebih sederhana belum menjamin jawaban akurat atau kemampuan mengikuti instruksi. Ini model eksperimen, bukan asisten produksi.

Periksa kartu dataset dan ketentuan lisensi/atribusi sumber sebelum mendistribusikan ulang teks hasil ekstraksi.
