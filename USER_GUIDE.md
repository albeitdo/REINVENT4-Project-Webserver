# 📘 Panduan Pengguna (User Guide) - REINVENT 4 Web Portal

Selamat datang di **REINVENT 4 Web Portal**! Panduan ini dirancang untuk membantu Anda (peneliti farmasi, kimiawan, maupun akademisi) merancang dan mengoptimasi molekul obat baru secara visual tanpa perlu memahami kode pemrograman atau baris perintah (*command line*).

---

## 📑 Daftar Isi
1. [Alur Singkat Penemuan Obat](#-alur-singkat-penemuan-obat)
2. [Memulai & Memilih Bahasa](#1-memulai--memilih-bahasa)
3. [Tahap 1: Membersihkan Dataset (Pre-processing)](#2-tahap-1-membersihkan-dataset-pre-processing)
4. [Tahap 2: Melatih Model ke Target Tertentu (Transfer Learning)](#3-tahap-2-melatih-model-ke-target-tertentu-transfer-learning)
5. [Tahap 3: Mengoptimasi Sifat Obat (Staged Learning / RL)](#4-tahap-3-mengoptimasi-sifat-obat-staged-learning--rl)
6. [Tahap 4: Menghasilkan & Mengevaluasi Molekul (Sampling)](#5-tahap-4-menghasilkan--mengevaluasi-molekul-sampling)
7. [Memantau Status & Riwayat Pekerjaan (Job Tracking)](#6-memantau-status--riwayat-pekerjaan-job-tracking)
8. [Tanya Jawab & Troubleshooting (FAQ)](#7-tanya-jawab--troubleshooting-faq)

---

## 🧭 Alur Singkat Penemuan Obat

Aplikasi ini menyusun siklus perancangan molekul ke dalam 4 langkah berurutan:

```
[ Dataset Molekul Mentah (.csv) ]
               │
               ▼
   [ 1. Pre-processing ] ──► Menyaring kotoran & menstandardisasi struktur (.smi)
               │
               ▼
 [ 2. Transfer Learning ] ──► Melatih AI agar fokus pada kelas molekul target (.prior)
               │
               ▼
 [ 3. Staged Learning (RL) ] ──► Mengoptimasi bobot kelayakan obat & berat molekul
               │
               ▼
      [ 4. Sampling ] ──► Memanen ribuan molekul baru + Analisis visual 2D
```

---

## 1. Memulai & Memilih Bahasa

1. Buka browser dan akses alamat portal (biasanya `http://localhost:8501`).
2. Di halaman **Welcome Screen**:
   - Terdapat ringkasan 4 fitur utama.
   - Pilih bahasa tampilan yang nyaman bagi Anda: **Indonesia** atau **English**.
3. Klik tombol **"Mulai"** (atau **"Start"**) untuk masuk ke ruang kerja.
   *(Pilihan bahasa juga dapat Anda ubah kapan saja melalui menu di sidebar).*

---

## 2. Tahap 1: Membersihkan Dataset (Pre-processing)

Sebelum melatih AI, dataset senyawa kimia (misalnya hasil unduhan dari ChEMBL atau PubChem) harus dibersihkan dari molekul garam atau senyawa yang tidak realistis.

### Cara Menggunakan:
1. Klik menu **Pre-processing** pada sidebar.
2. **Unggah Dataset**: Masukkan file `.csv` yang berisi struktur molekul SMILES.
   > **Catatan Praktis**: Anda tidak perlu pusing mengubah nama kolom. Sistem otomatis mengenali kolom apakah bernama `SMILES`, `Smiles`, atau `smiles`.
3. **Atur Parameter Penyaringan**:
   - **Min & Max Heavy Atoms**: Batas jumlah atom non-hidrogen (default: 2 sampai 90 atom).
   - **Max Molecular Weight**: Batas atas berat molekul (default: 1200 Dalton untuk menyingkirkan polimer besar).
   - **Uncharge Molecules (Centang)**: Otomatis menetralkan molekul bermuatan/garam menjadi bentuk netral stabil.
   - **Keep Stereochemistry (Centang)**: Mempertahankan konfigurasi kiralitas ruang ($R/S$).
4. Klik tombol **"Mulai Pre-processing"**.
5. **Hasil**:
   - Muncul informasi jumlah senyawa yang berhasil lolos kriteria.
   - Tabel pratinjau 20 struktur SMILES pertama.
   - Tombol **"Download Hasil (.smi)"** untuk mengunduh file bersih yang siap dipakai di tahap selanjutnya.

---

## 3. Tahap 2: Melatih Model ke Target Tertentu (Transfer Learning)

Model dasar bawaan REINVENT (*Base Prior*) dilatih dari jutaan molekul umum. Fitur ini digunakan untuk **mengajarkan AI mengenali kelas molekul spesifik** yang Anda teliti (misalnya senyawa inhibitor kinase, antikanker, dsb).

### Cara Menggunakan:
1. Klik menu **Transfer Learning** pada sidebar.
2. **Pilih Base Model**:
   - Gunakan model bawaan seperti `De Novo — reinvent (.reinvent)` untuk molekul obat standar.
   - Atau centang opsi upload jika Anda memiliki file model `.prior` sendiri.
3. **Unggah Dataset Latih**:
   - Masukkan file `.csv` atau `.smi` hasil dari tahap Pre-processing.
   - *Ingin coba cepat?* Klik tombol **"Muat Data Contoh"** untuk langsung memuat 30 senyawa uji coba siap pakai.
4. **Validation Split (Pemisahan Validasi Otomatis)**:
   - Geser slider persentase validasi (rekomendasi: **20%**).
   - Sistem akan otomatis membagi data menjadi data latih dan data uji tanpa Anda harus memecahnya secara manual di Excel.
5. **Parameter Pelatihan**:
   - **Epochs**: Jumlah perulangan belajar model (rekomendasi: 10–20 epoch untuk pengujian cepat di laptop).
   - **Batch Size**: Jumlah molekul yang diproses per iterasi (default: 32).
6. Klik **"Mulai Transfer Learning"**.
7. **Hasil**: Setelah selesai, Anda dapat mengunduh model baru bernama `finetuned.prior` (~23 MB). Simpan file ini untuk dipakai pada tahap RL atau Sampling.

---

## 4. Tahap 3: Mengoptimasi Sifat Obat (Staged Learning / RL)

Tahap ini menggunakan *Reinforcement Learning* untuk mengarahkan model menghasilkan molekul yang memiliki sifat fisikokimia obat ideal (*Drug-likeness*).

### Setup Model (Kiri vs Kanan):
Halaman ini dirancang menggunakan konfigurasi **Dual-Model**:
- **Kolom Kiri - Prior Model (Pengawas)**: Pilih model bawaan `De Novo — reinvent`. Model ini bertindak sebagai "pagar pembatas" agar molekul tidak menyimpang menjadi struktur yang mustahil disintesis.
- **Kolom Kanan - Agent Model (Aktor yang Dioptimasi)**: Unggah file model `.prior` hasil dari tahap **Transfer Learning** Anda.

### Parameter Optimasi:
- **Max Steps**: Jumlah langkah iterasi optimasi (misal: 50–100 langkah).
- **QED Weight**: Bobot untuk memaksimalkan *Quantitative Estimate of Drug-likeness* (nilai antara 0.0 – 10.0; nilai default 1.0 sudah sangat baik).
- **Min MW & Max MW**: Rentang massa molekul yang Anda targetkan (contoh: 250 – 450 Da untuk molekul obat oral kecil).
- Klik tombol **"Mulai Optimasi (RL)"**.
- **Hasil**: Sistem akan memproduksi model checkpoint teroptimasi (`stage1.chkpt` / `.prior`) dan tabel evaluasi bertahap.

---

## 5. Tahap 4: Menghasilkan & Mengevaluasi Molekul (Sampling)

Setelah model Anda terfokus dan teroptimasi, saatnya memanen kandidat molekul obat baru!

### Cara Menggunakan:
1. Klik menu **Sampling** pada sidebar.
2. **Pilih Model**:
   - Bisa menggunakan model bawaan, model hasil Transfer Learning, atau model hasil RL.
3. **Jumlah Molekul (Number of SMILES)**: Masukkan jumlah molekul yang ingin dirancang (contoh: 50 hingga 1000 molekul).
4. **Perbandingan Kemiripan (Tanimoto Similarity)**:
   - Masukkan struktur SMILES senyawa obat pembanding pada kolom referensi.  
     *(Contoh: ketik `CC(=O)Oc1ccccc1C(=O)O` untuk membandingkan kemiripannya dengan Aspirin).*
5. Klik **"Mulai Sampling"**.

### Cara Membaca Dashboard Hasil:
Setelah selesai, sistem secara otomatis menghitung metrik kualitas dengan bantuan RDKit:
- 🟢 **Validity Rate (%)**: Persentase molekul yang valid mematuhi hukum valensi kimia nyata. Nilai yang baik biasanya di atas 90%.
- 🔵 **Uniqueness Rate (%)**: Mengukur keberagaman molekul. Jika nilainya tinggi (>80%), berarti AI kreatif dan tidak mengalami *mode collapse* (tidak mengulang molekul yang sama).
- 🖼️ **Galeri Visual 2D**: Menampilkan gambar 2D diagram struktur kimia untuk senyawa-senyawa terbaik.
- 💾 **Download CSV**: Unduh seluruh daftar molekul baru beserta nilai skor kemiripannya untuk analisis penambatan molekuler (*molecular docking*).

---

## 6. Memantau Status & Riwayat Pekerjaan (Job Tracking)

Karena pelatihan *neural network* membutuhkan waktu:
- **Live Job Status (Sidebar)**: Anda bisa melihat apakah proses berstatus `QUEUED` (antri), `RUNNING` (sedang komputasi), `COMPLETED` (selesai), atau `FAILED` (gagal).
- **Riwayat Job**: Semua pekerjaan tersimpan dalam kotak riwayat di sidebar. 
- Anda dapat mengklik tombol **"Lihat Hasil"** pada riwayat masa lalu untuk membuka kembali tabel atau gambar molekul kapan saja tanpa takut data hilang.
- Gunakan tombol **"Tutup"** untuk melipat kembali tampilan hasil jika ingin ruang kerja bersih kembali.

---

## 7. Tanya Jawab & Troubleshooting (FAQ)

**Q: Apakah laptop saya akan membeku (*freeze*) saat proses training berjalan?**  
*A: Tidak. Web server menggunakan arsitektur pemrosesan latar belakang (asinkron), sehingga Anda tetap dapat membuka halaman web lain dengan lancar.*

**Q: Kenapa status job saya FAILED saat Pre-processing?**  
*A: Pastikan file yang diunggah berformat `.csv` dan di dalamnya terdapat kolom berisi deretan teks molekul SMILES yang valid.*

**Q: Di mana file-file hasil kerja saya tersimpan secara fisik?**  
*A: Semua file dataset, konfigurasi `.toml`, dan model hasil tersimpan terorganisir per ID pekerjaan di dalam folder `web_server/jobs/{job_id}/` di komputer Anda.*

**Q: Bisakah saya langsung melakukan Sampling tanpa Transfer Learning?**  
*A: Bisa! Anda bisa langsung ke menu Sampling dan memilih model bawaan (`reinvent.prior`) untuk mengeksplorasi molekul de novo secara bebas.*
