# 🧪 REINVENT 4 Web Portal: Generative Drug Design Platform

Antarmuka web interaktif berbasis **Streamlit** dan **FastAPI** untuk **REINVENT 4** (AstraZeneca). Dirancang untuk mendemokratisasi penemuan obat berbasis kecerdasan buatan (*AI-driven De Novo Drug Discovery*) tanpa perlu mengetik perintah terminal (*CLI*) maupun menyusun konfigurasi *TOML* secara manual.

---

## 🌟 Fitur Utama

1. **Data Pre-processing Pipeline**  
   - Pembersihan & filter dataset molekul SMILES otomatis (berat molekul, atom berat, netralisasi muatan/uncharge, stereokimia).
   - *Smart Column Detection*: Otomatis mendeteksi variasi penulisan kolom seperti `SMILES`, `Smiles`, atau `smiles`.
   - Pratinjau 20 baris pertama & download file `.smi` bersih siap training.

2. **Transfer Learning (Finetuning Prior)**  
   - Adaptasi model dasar (*base prior*) agar fokus meniru kelas senyawa target peneliti.
   - *Dynamic Validation Split*: Cukup upload 1 file CSV, sistem otomatis mengacak dan membaginya menjadi data latih dan validasi (slider proporsi 5% – 50%).
   - Tersedia tombol **"Muat Data Contoh"** (30 senyawa bioaktif) untuk uji coba instan.

3. **Staged Learning (Reinforcement Learning)**  
   - Optimasi berbasis fungsi *reward* (*Multi-Component Geometric Mean*).
   - Pengaturan bobot kelayakan obat (*QED Weight*), rentang berat molekul sasaran (*Min & Max MW*), dan *Max Steps*.
   - **Arsitektur Dual-Model**:
     - **Prior (Kiri)**: Model dasar umum sebagai "pagar pengawas" agar struktur kimia tetap realistis.
     - **Agent (Kanan)**: Model hasil Transfer Learning yang aktif dieksplorasi dan dioptimasi.

4. **Sampling & Evaluasi Kualitas Molekul (RDKit)**  
   - Generasi ratusan hingga ribuan kandidat molekul baru (*De Novo Sampling*).
   - Evaluasi kimiawi otomatis:
     - **Validity Rate (%)**: Persentase molekul yang mematuhi hukum ikatan/valensi kimia.
     - **Uniqueness Rate (%)**: Mengukur keberagaman molekul guna mendeteksi *mode collapse*.
     - **Tanimoto Similarity Index**: Mengukur kemiripan struktur terhadap molekul obat referensi (Morgan Fingerprints).
   - Visualisasi gambar 2D molekul langsung di browser dan ekspor tabel CSV.

5. **UX & Developer Experience**  
   - **Bilingual Interface**: Tersedia opsi Bahasa Indonesia & English yang dapat diubah secara instan.
   - **Live Job Tracking**: Pelacak status tugas latar belakang (*QUEUED, RUNNING, COMPLETED, FAILED*).
   - **Scrollable Job History**: Riwayat tugas tersimpan permanen per UUID di folder `jobs/` dan dapat dilihat kembali kapan saja.

---

## 🏗️ Arsitektur Sistem

Aplikasi ini menggunakan arsitektur *decoupled full-stack*:
- **Frontend**: Streamlit (`port 8501`) untuk rendering visual dan interaksi pengguna.
- **Backend**: FastAPI (`port 8000`) dengan fitur *BackgroundTasks* untuk menangani eksekusi REINVENT 4 secara asinkron tanpa membekukan antarmuka web.
- **Engine**: REINVENT 4 core library + PyTorch + RDKit.

---

## 🚀 Panduan Menjalankan Aplikasi Secara Lokal

### Prasyarat
- Python 3.10 atau 3.11
- Git (opsional)

### 1. Menjalankan Server Otomatis (Windows)
Cukup jalankan script batch terpadu yang ada di folder `web_server`:
```powershell
cd web_server
.\start_all.bat
```
Script tersebut akan menyalakan **API Server (Port 8000)** dan **Web UI (Port 8501)** secara bersamaan.

### 2. Membuka di Browser
- **Aplikasi Web**: [http://localhost:8501](http://localhost:8501)
- **Dokumentasi API Swagger**: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 📖 Tutorial & Alur Demo Langkah Demi Langkah

Berikut panduan skenario demo penemuan obat dari awal hingga akhir:

### Langkah 1: Sambutan & Pilihan Bahasa
1. Buka [http://localhost:8501](http://localhost:8501).
2. Di halaman **Welcome Screen**, pilih bahasa yang Anda inginkan (**Indonesia** / **English**).
3. Klik tombol **"Mulai"** / **"Start"** untuk masuk ke portal kerja.

### Langkah 2: Pre-processing Dataset SMILES
1. Pada menu sidebar, pilih **Pre-processing**.
2. Unggah file dataset senyawa Anda (format `.csv` yang memiliki kolom SMILES).
3. Atur parameter batas atom dan berat molekul sesuai kebutuhan.
4. Klik **"Mulai Pre-processing"**.
5. Amati status di sidebar **Live Job Status**. Setelah selesai, klik **"Lihat Hasil"** untuk melihat total molekul yang lolos filter dan download file `processed.smi`.

### Langkah 3: Transfer Learning (Finetuning Model)
1. Pilih menu **Transfer Learning**.
2. Pilih model dasar pada dropdown (contoh: `De Novo — reinvent (.reinvent)`).
3. Unggah file hasil pre-processing atau klik tombol **"Muat Data Contoh"**.
4. Tentukan persentase data validasi menggunakan slider (misal 20%).
5. Atur jumlah **Epochs** (misal 10–20 untuk pengujian cepat) dan klik **"Mulai Transfer Learning"**.
6. Setelah selesai, download file model baru `finetuned.prior`.

### Langkah 4: Staged Learning (Reinforcement Learning)
1. Pilih menu **Staged Learning (RL)**.
2. Pada kolom **Pilih Prior (Kiri)**: Pilih model bawaan `De Novo — reinvent`.
3. Pada kolom **Pilih Agent (Kanan)**: Unggah file model hasil Transfer Learning (`finetuned.prior`) yang Anda peroleh dari Langkah 3.
4. Tentukan target profil obat:
   - **QED Weight**: 1.0 (atau lebih tinggi untuk mengutamakan kemiripan obat).
   - **Min MW & Max MW**: Misal rentang 250 – 450 Da.
   - **Max Steps**: Misal 50–100 langkah.
5. Klik **"Mulai Optimasi (RL)"**. Sistem akan mengarahkan generasi struktur ke target sifat yang ditentukan.

### Langkah 5: Sampling & Panen Molekul
1. Pilih menu **Sampling**.
2. Pilih model yang ingin di-generate (bisa model Base, hasil TL, atau hasil RL).
3. Tentukan jumlah molekul yang ingin dibuat (misal 100 senyawa).
4. *(Opsional)* Masukkan struktur SMILES pembanding pada kolom **Tanimoto Reference SMILES** (misal: `CC(=O)Oc1ccccc1C(=O)O` untuk Aspirin).
5. Klik **"Mulai Sampling"**.
6. **Hasil**:
   - Dashboard akan menampilkan metrik **Validity %** dan **Uniqueness %**.
   - Galeri gambar 2D struktur senyawa akan muncul otomatis.
   - Tabel perolehan molekul lengkap beserta skor kemiripannya dapat langsung diunduh dalam format `.csv`.

---

## 📂 Struktur Direktori Proyek

```text
REINVENT/
├── requirements.txt            # Daftar dependensi untuk deployment
├── .gitignore                  # Filter direktori virtualenv & file job
├── web_server/
│   ├── ui.py                   # Frontend Streamlit utama
│   ├── api.py                  # Backend FastAPI
│   ├── toml_builder.py         # Generator konfigurasi TOML REINVENT
│   ├── job_manager.py          # Pengelola proses asinkron & status job
│   ├── translations.py         # Kamus translasi dwibahasa (ID/EN)
│   ├── start_all.bat           # Script otomatisasi peluncuran lokal
│   ├── jobs/                   # Tempat penyimpanan hasil komputasi (per UUID)
│   └── samples/                # Dataset contoh untuk testing
└── REINVENT4-main/             # Source code inti library REINVENT 4
    ├── reinvent/               # Modul neural network & algoritma generatif
    └── priors/                 # Model-model prior bawaan (.prior)
```

---

## 👥 Kontributor & Lisensi
- Dikembangkan untuk keperluan penelitian dan pemanfaatan komputasi farmasi.
- Didukung oleh modul inti **REINVENT 4** (AstraZeneca, lisensi Apache 2.0).
