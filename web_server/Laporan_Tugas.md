# Laporan Tugas: Implementasi Web Server untuk REINVENT 4

## 1. Pendahuluan
Aplikasi ini adalah antarmuka berbasis web (Web UI) untuk **REINVENT 4**, sebuah perangkat lunak berbasis Kecerdasan Buatan (AI) yang lazim digunakan dalam kimia komputasi dan penemuan obat (*drug discovery*). 

Dengan adanya web server ini, pengguna tidak perlu lagi berurusan dengan perintah terminal (CLI) yang rumit. Semua proses desain dan optimasi molekul dapat dilakukan melalui antarmuka visual yang interaktif (Streamlit) yang terhubung langsung ke mesin pemroses (FastAPI).

## 2. Fitur & Kegunaan Utama
REINVENT 4 yang disematkan dalam web server ini memiliki beberapa fungsi utama:
- **De Novo Design:** Kemampuan AI (menggunakan *Reinforcement Learning*) untuk merancang struktur obat atau molekul kecil yang sama sekali baru dari nol.
- **Molecule Optimization:** Mengoptimalkan struktur molekul yang sudah ada agar memenuhi kriteria sifat kimia dan biologi yang diinginkan (profil *scoring* multi-komponen).
- **Scaffold Hopping & R-group Replacement:** Mengeksplorasi dan memodifikasi variasi kerangka utama molekul untuk mencari kandidat molekul dengan aktivitas biologis yang lebih kuat atau efek samping yang lebih sedikit.

## 3. Arsitektur Sistem
Sistem ini dirancang dengan memisahkan bagian tampilan dan pemrosesan:
1. **Frontend (Tampilan Web):** Menggunakan *Streamlit*. Bertugas untuk menerima *input* dari pengguna (seperti parameter molekul) dan menampilkan hasil (*output*) secara visual.
2. **Backend (API Server):** Menggunakan *FastAPI*. Bertugas sebagai jembatan yang mengirimkan *input* pengguna ke mesin REINVENT 4, mengatur antrean tugas (*job manager*), dan mengembalikan hasil kalkulasi ke Frontend.

## 4. Screenshot Aplikasi
*(Catatan: Silakan hapus teks ini dan masukkan gambar/screenshot web Anda di sini)*

- **Gambar 1:** Tampilan Beranda Web Server REINVENT.
- **Gambar 2:** Tampilan saat memasukkan parameter (Input).
- **Gambar 3:** Tampilan hasil (*output*) desain molekul yang berhasil dibuat oleh AI.

## 5. Panduan Menjalankan Sistem Secara Lokal
Untuk menjalankan sistem ini secara lokal di laptop administrator:
1. Masuk ke direktori proyek `web_server`.
2. Klik ganda pada file **`start_all.bat`**.
3. Sistem secara otomatis akan menjalankan *Virtual Environment* bawaan dan menyalakan API Server (Port 8000) serta Web UI (Port 8501) secara bersamaan.
4. Akses melalui browser pada alamat: `http://localhost:8501`.
