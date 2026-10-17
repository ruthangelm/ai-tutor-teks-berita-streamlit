# AI Tutor Bahasa Indonesia — Teks Berita

Aplikasi pembelajaran interaktif berbasis Streamlit untuk materi teks berita kelas XI.

## Fitur yang ada
- Tema ruang redaksi digital dengan warna biru dan aksen keemasan.
- Ruang akses Siswa dan Guru.
- Beranda, petunjuk penggunaan, materi, evaluasi, dan rubrik penilaian untuk siswa.
- Beranda guru, perangkat ajar, bank soal, rubrik guru, dan petunjuk guru.
- Materi teks berita, soal pilihan ganda, dan pembahasan jawaban.
- Dukungan dokumen materi `.txt` dalam folder `database/` untuk pencarian jawaban berbasis materi.

## Menjalankan di komputer
1. Pasang Python 3.10 atau yang lebih baru.
2. Buka terminal di folder proyek.
3. Jalankan `pip install -r requirements.txt`.
4. Jalankan `streamlit run app.py`.

## Publikasi online
Aplikasi ini menggunakan Streamlit, jadi **tidak bisa dijalankan langsung oleh GitHub Pages**. Gunakan layanan hosting yang mendukung Streamlit, misalnya Streamlit Community Cloud:
1. Unggah `app.py`, `requirements.txt`, folder `database/`, dan `README.md` ke repositori GitHub.
2. Buka https://share.streamlit.io/ atau Streamlit Community Cloud melalui situs resmi Streamlit dan masuk menggunakan GitHub.
3. Pilih repositori, branch `main`, dan file utama `app.py`.
4. Deploy aplikasi. Setelah selesai, layanan akan memberikan URL aplikasi.

## Catatan penting
- Aplikasi saat ini memiliki materi dan evaluasi yang ditulis di dalam `app.py`.
- Fungsi tanya tutor mengambil potongan jawaban dari dokumen `.txt` yang ada di folder `database/`; ini bukan AI generatif penuh.
- Jangan menaruh kata sandi atau API key di `app.py` atau repositori publik.
- Pilihan peran Guru/Siswa pada versi ini bukan sistem autentikasi dan belum menyimpan hasil ke basis data bersama.
