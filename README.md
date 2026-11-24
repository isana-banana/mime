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

train.py memeriksa jumlah parameter dan menghentikan training bila tidak tepat 298.656.

## Strategi korpus: percakapan dulu

Korpus lama dari vickyfatrian/vqfat-indo-corpus (teks cerita/penjelasan) tidak lagi dipakai untuk training chatbot. Audit sebelumnya menunjukkan gaya yang kaku dan tidak cocok sebagai dasar utama percakapan sehari-hari.

Kandidat korpus baru menggabungkan tiga sumber yang memiliki lisensi MIT pada kartu dataset:

1. LorthGyu/indonesian-chat — percakapan multi-turn dengan gaya santai, campuran, dan formal; topik sehari-hari.
2. LorthGyu/indonesian-dialogue-scenarios — dialog situasional seperti pasar, rumah, kantor, sekolah, warung, stasiun, dan bengkel.
3. daruokta/t5gemma2-indonesia-chat-formatted, subset chat_multiturn — percakapan multi-turn dan instruksi bahasa Indonesia.

Sumber:
- https://huggingface.co/datasets/LorthGyu/indonesian-chat
- https://huggingface.co/datasets/LorthGyu/indonesian-dialogue-scenarios
- https://huggingface.co/datasets/daruokta/t5gemma2-indonesia-chat-formatted

prepare_data.py mengambil hanya pesan user/assistant (system prompt dibuang), menjaga urutan percakapan, menyeragamkan label pembicara, menyaring teks rusak/berulang/campur bahasa berlebihan, dan menghapus duplikasi. Dari sumber LorthGyu, contoh bergaya formal sengaja dilewati; yang diprioritaskan adalah gaya santai dan campuran. Dataset dialog situasional diberi label generik Pembicara 1/2 agar nama tokoh tidak menjadi pola utama.

**Penting:** dataset percakapan publik tersebut tetap bisa berisi teks buatan, salah ketik, atau percakapan yang kurang alami. Filter otomatis hanya membuang noise yang jelas; filter tidak bisa menilai rasa bahasa dengan sempurna. Karena itu workflow audit menghasilkan sampel acak per sumber (audit/samples_by_source.txt), dialog skenario terpisah (audit/scenario_candidates.txt), dan laporan (audit/report.json). Sampel harus ditinjau manusia sebelum training.

## Korpus sintetis orisinal

Batch awal percakapan buatan AI disimpan terpisah di `data/synthetic/seed_v1.jsonl` (25 percakapan). Batch ini belum dipakai training. Aturan pembuatan dan gerbang review ada di `data/synthetic/README.md`. Batch berikutnya hanya ditambahkan setelah format, variasi gaya, duplikasi, dan sampel kualitasnya diperiksa.

## Audit korpus

Buka tab Actions → Audit MIME-ID conversation corpus → Run workflow. Artefak mime-id-conversation-corpus-audit berisi:
- audit/report.json: jumlah data per sumber dan alasan penolakan
- audit/samples_by_source.txt: contoh acak yang diterima dari setiap sumber
- data/candidate.txt: kandidat korpus lengkap

## Training

Training dibuat manual saja agar perubahan filter atau sumber data tidak otomatis memulai training sebelum audit diperiksa.

Buka tab Actions → Train MIME-ID 300K → Run workflow. Default: 6.000 langkah dan batch size 32. Workflow membangun ulang korpus dengan pipeline yang sama, lalu melatih model dan mengunggah best.pt serta last.pt.

## Batasan

Model 300K sangat kecil. Panjang konteks 128 byte juga membatasi seberapa banyak percakapan yang bisa dipahami sekaligus. Korpus yang lebih baik dapat memperbaiki gaya bahasa, tetapi tidak otomatis membuat model akurat atau mampu mengikuti instruksi kompleks. Model ini tetap eksperimen, bukan asisten produksi.

Periksa lisensi sumber dan ketentuan atribusi sebelum mendistribusikan ulang korpus hasil gabungan.
