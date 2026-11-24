# Data MIME-ID 300K

Workflow mengambil sumber dari `vickyfatrian/vqfat-indo-corpus` konfigurasi `cosmopedia_id`, lalu menyaringnya melalui `prepare_data.py`.

Fokus korpus:
- Bahasa Indonesia umum dan kalimat yang relatif pendek.
- Topik keseharian seperti keluarga, rumah, sekolah, pekerjaan, makanan, tempat, kegiatan, dan cerita.
- Potongan sekitar 15–90 kata agar sesuai dengan model byte-level berkonteks 128 token.

Skrip membersihkan URL, HTML, karakter kontrol, dan duplikasi. Filter kosakata adalah heuristik sederhana; hasilnya perlu diperiksa karena tidak dapat menjamin seluruh teks benar-benar sederhana atau alami.

Jangan masukkan data pribadi, rahasia, atau teks yang tidak memiliki izin untuk digunakan sebagai data pelatihan. Ikuti lisensi dan atribusi dataset sumber.
