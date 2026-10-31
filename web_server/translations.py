STRINGS = {
    "id": {
        # Landing page
        "landing_title": "REINVENT 4 Web Interface",
        "landing_subtitle": "Antarmuka grafis berbasis web untuk menjalankan pipeline generasi molekul menggunakan <strong>REINVENT 4</strong> — tanpa harus mengetik perintah CLI secara manual.",
        "feat_preprocessing": "Pre-processing",
        "feat_preprocessing_desc": "Filter dan normalisasi dataset SMILES sebelum digunakan untuk training.",
        "feat_tl": "Transfer Learning",
        "feat_tl_desc": "Lakukan fine-tuning model prior menggunakan dataset molekul referensi Anda.",
        "feat_rl": "Staged Learning (RL)",
        "feat_rl_desc": "Optimasi model menggunakan reinforcement learning berdasarkan target QED dan berat molekul.",
        "feat_sampling": "Sampling",
        "feat_sampling_desc": "Generate molekul-molekul baru dan evaluasi kualitasnya secara otomatis.",
        "enter_btn": "Mulai",
        "language_label": "Bahasa / Language",

        # Sidebar
        "sidebar_title": "REINVENT 4 Portal",
        "sidebar_mode_label": "Pilih Mode Komputasi",
        "mode_preprocessing": "Pre-processing",
        "mode_tl": "Transfer Learning",
        "mode_rl": "Staged Learning (RL)",
        "mode_sampling": "Sampling",
        "sidebar_live_status": "Status Job Aktif",
        "sidebar_history": "Riwayat Job",
        "no_active_job": "Belum ada job yang berjalan saat ini.",
        "no_history": "Belum ada riwayat yang tersimpan.",
        "status_queued": "Antri...",
        "status_running": "Sedang berjalan...",
        "status_completed": "Selesai!",
        "status_failed": "Gagal.",
        "btn_refresh": "Refresh Status",
        "btn_view": "Lihat Hasil",

        # Preprocessing
        "pre_header": "Pre-processing Dataset",
        "pre_info": "Filter dan bersihkan dataset SMILES Anda sebelum digunakan untuk Transfer Learning. Menggunakan reinvent.datapipeline.",
        "pre_upload_label": "Upload Dataset",
        "pre_upload": "Upload file CSV (harus ada kolom SMILES)",
        "pre_params": "Parameter Filter",
        "pre_min_heavy": "Min Heavy Atoms",
        "pre_max_heavy": "Max Heavy Atoms",
        "pre_max_mw": "Max Molecular Weight (Da)",
        "pre_stereo": "Pertahankan Stereokimia",
        "pre_uncharge": "Netralkan Muatan (Uncharge)",
        "pre_run_btn": "Jalankan Preprocessing",
        "pre_no_file": "Harap upload file CSV terlebih dahulu.",
        "pre_sending": "Mengirim job preprocessing...",
        "pre_started": "Job dimulai! ID: {}... Pantau status di sidebar.",
        "pre_conn_fail": "Gagal koneksi ke API: {}",
        "pre_result_title": "Preprocessing Selesai!",
        "pre_result_metric": "Jumlah Molekul Valid Setelah Filter",
        "pre_result_preview": "Preview 20 SMILES Pertama",
        "pre_no_smi": "File processed.smi belum ditemukan.",
        "pre_download": "Download Hasil Preprocessing (.smi)",
        "pre_download_info": "File .smi yang diunduh bisa langsung digunakan sebagai dataset Transfer Learning.",

        # Transfer Learning
        "tl_header": "Transfer Learning",
        "tl_prior_label": "Pilih Prior",
        "tl_prior_builtin": "Gunakan prior bawaan",
        "tl_prior_custom": "Upload prior sendiri",
        "tl_upload_prior": "Upload file prior (.prior)",
        "tl_upload_dataset": "Upload Dataset CSV",
        "tl_epochs": "Jumlah Epoch",
        "tl_batch": "Batch Size",
        "tl_val_split_toggle": "Gunakan Validation Split",
        "tl_val_split_toggle_help": "Aktifkan jika ingin memisahkan sebagian dataset sebagai data validasi. Disarankan untuk De Novo (Reinvent). Tidak wajib untuk LibInvent/LinkInvent.",
        "tl_val_split": "Proporsi Validation Split",
        "tl_val_split_help": "Contoh: 0.20 berarti 20% data digunakan sebagai validasi, 80% untuk training.",
        "tl_run_btn": "Jalankan Transfer Learning",
        "tl_result_title": "Transfer Learning Selesai!",
        "tl_download": "Download Model Finetuned (.prior)",

        # RL
        "rl_header": "Staged Learning (Reinforcement Learning)",
        "rl_prior_label": "Pilih Prior (Base Model)",
        "rl_agent_label": "Pilih Agent (Hasil TL / Base)",
        "rl_upload_custom": "Atau upload Prior Anda (.prior)",
        "rl_upload_agent": "Atau upload Agent Anda (.prior)",
        "rl_max_steps": "Max Steps",
        "rl_qed_weight": "QED Weight",
        "rl_mw_min": "Min Molecular Weight",
        "rl_mw_max": "Max Molecular Weight",
        "rl_run_btn": "Mulai Optimasi (RL)",
        "rl_result_title": "Optimasi Staged Learning (RL) Selesai!",
        "rl_csv_wait": "Menunggu hasil CSV ditulis oleh REINVENT...",
        "rl_download": "Download Model Hasil RL (.prior)",

        # Sampling
        "samp_header": "Sampling",
        "samp_prior_label": "Pilih Prior",
        "samp_num_smiles": "Jumlah Molekul yang Di-generate",
        "samp_run_btn": "Jalankan Sampling",
        "samp_ref_smi": "Masukkan SMILES Referensi (opsional, untuk hitung Tanimoto Similarity):",
        "samp_tanimoto_spin": "Menghitung Tanimoto Similarity...",
        "samp_result_metric_total": "Total Output",
        "samp_result_metric_valid": "Validity",
        "samp_result_metric_unique": "Uniqueness",
        "samp_eval_header": "Evaluasi Metrik Generasi",
        "samp_download": "Download CSV",
        "samp_no_file": "File hasil (sampling.csv) belum tersedia.",

        # Result viewer
        "result_close": "Tutup",
        "result_expander": "Tampilkan / Sembunyikan Hasil",
        "result_header": "Hasil Job",
        "tl_example_loaded": "Data contoh dimuat.",
        "samp_example_loaded": "Parameter contoh dimuat. Klik Jalankan Sampling.",
        "samp_header_title": "Sampling — Eksplorasi Ruang Kimia",
        "samp_show_2d": "🔬 Tampilkan Gambar 2D Molekul (10 Pertama)",
        "file_selected": "File terpilih",

        "api_http_error": "Server API error {}: {}",

        "check_log": "Cek run.log di folder job.",

        "job_sent": "Job dikirim!",

        "pre_max_mw_help": "Berat molekul maksimum yang diizinkan (Dalton).",

        "pre_max_heavy_help": "Jumlah maksimum atom berat.",

        "pre_min_heavy_help": "Jumlah minimum atom berat (non-hidrogen) dalam molekul.",

        "rl_upload_custom": "Atau upload model Prior Anda sendiri (.prior)",

        "tl_preview_example": "Pratinjau Data Contoh (5 baris pertama)",

        "tl_download_example": "Download File Contoh (.csv)",

        "tl_example_active": "{} molekul aktif sebagai data contoh — `{}`",

        "pre_uncharge_help": "Normalkan muatan formal molekul menjadi netral jika memungkinkan.",

        "pre_stereo_help": "Jika dicentang, informasi stereokimia (R/S) dipertahankan.",

        "api_conn_fail": "Gagal koneksi ke API: {}",

        "tl_no_dataset": "Harap upload file dataset CSV atau klik 'Muat Data Contoh' terlebih dahulu.",

        "tl_example_info": "File contoh di atas akan digunakan sebagai dataset jika Anda tidak mengupload file sendiri.",

        "tl_example_download_help": "Unduh file contoh ini sebagai referensi format yang dibutuhkan",

        "tl_load_example_help": "Memuat 30 molekul drug-like sebagai contoh dataset",

        "tl_load_example": "Muat Data Contoh",

        "tl_csv_hint": "File CSV harus memiliki kolom bernama `SMILES`. Maks 10 MB.",

        "tl_custom_caption": "Upload file prior custom sebagai titik awal finetuning.",

        "tl_tab_custom": "Upload Base Model Custom",

        "tl_tab_builtin": "Built-in Prior sebagai Base",

        "tl_caption": "Finetune model prior menggunakan dataset Anda. Output berupa model `.prior` baru yang bisa dipakai untuk Sampling.",

        "samp_load_example_help": "Mengisi parameter dengan nilai rekomendasi untuk percobaan cepat",

        "samp_load_example": "Muat Parameter Contoh",

        "samp_upload_model_help": "Jika diisi, file ini diprioritaskan di atas pilihan Built-in Prior.",

        "samp_upload_model": "Upload file model",

        "samp_custom_caption": "Upload file model Anda sendiri (hasil Transfer Learning, checkpoint, dll).",

        "samp_tab_custom": "Upload Model Custom (.prior / .pt / .ckpt)",

        "samp_tab_builtin": "Built-in Prior",

        "samp_caption": "Generate molekul baru menggunakan pre-trained prior atau checkpoint custom Anda.",

        "rl_csv_cant_display": "File CSV ditemukan namun tidak dapat ditampilkan sebagai tabel.",

        "samp_ref_placeholder": "C1=CC=CC=C1",

        "api_error": "Gagal menghubungi API. Pastikan server berjalan.",
        "job_not_found": "Job tidak ditemukan di server.",
    },

    "en": {
        # Landing page
        "landing_title": "REINVENT 4 Web Interface",
        "landing_subtitle": "A web-based graphical interface for running molecular generation pipelines using <strong>REINVENT 4</strong> — without typing CLI commands manually.",
        "feat_preprocessing": "Pre-processing",
        "feat_preprocessing_desc": "Filter and normalize your SMILES dataset before using it for training.",
        "feat_tl": "Transfer Learning",
        "feat_tl_desc": "Fine-tune a prior model using your reference molecule dataset.",
        "feat_rl": "Staged Learning (RL)",
        "feat_rl_desc": "Optimize the model using reinforcement learning towards target QED and molecular weight.",
        "feat_sampling": "Sampling",
        "feat_sampling_desc": "Generate new molecules and automatically evaluate their quality.",
        "enter_btn": "Start",
        "language_label": "Language / Bahasa",

        # Sidebar
        "sidebar_title": "REINVENT 4 Portal",
        "sidebar_mode_label": "Select Computation Mode",
        "mode_preprocessing": "Pre-processing",
        "mode_tl": "Transfer Learning",
        "mode_rl": "Staged Learning (RL)",
        "mode_sampling": "Sampling",
        "sidebar_live_status": "Active Job Status",
        "sidebar_history": "Job History",
        "no_active_job": "No job is currently running.",
        "no_history": "No history saved yet.",
        "status_queued": "Queued...",
        "status_running": "Running...",
        "status_completed": "Completed!",
        "status_failed": "Failed.",
        "btn_refresh": "Refresh Status",
        "btn_view": "View Results",

        # Preprocessing
        "pre_header": "Dataset Pre-processing",
        "pre_info": "Filter and clean your SMILES dataset before Transfer Learning. Uses reinvent.datapipeline.",
        "pre_upload_label": "Upload Dataset",
        "pre_upload": "Upload CSV file (must have a SMILES column)",
        "pre_params": "Filter Parameters",
        "pre_min_heavy": "Min Heavy Atoms",
        "pre_max_heavy": "Max Heavy Atoms",
        "pre_max_mw": "Max Molecular Weight (Da)",
        "pre_stereo": "Keep Stereochemistry",
        "pre_uncharge": "Neutralize Charges (Uncharge)",
        "pre_run_btn": "Run Preprocessing",
        "pre_no_file": "Please upload a CSV file first.",
        "pre_sending": "Submitting preprocessing job...",
        "pre_started": "Job started! ID: {}... Monitor status in the sidebar.",
        "pre_conn_fail": "Failed to connect to API: {}",
        "pre_result_title": "Preprocessing Complete!",
        "pre_result_metric": "Valid Molecules After Filter",
        "pre_result_preview": "Preview First 20 SMILES",
        "pre_no_smi": "processed.smi file not found yet.",
        "pre_download": "Download Preprocessing Results (.smi)",
        "pre_download_info": "The downloaded .smi file can be used directly as a Transfer Learning dataset.",

        # Transfer Learning
        "tl_header": "Transfer Learning",
        "tl_prior_label": "Select Prior",
        "tl_prior_builtin": "Use built-in prior",
        "tl_prior_custom": "Upload custom prior",
        "tl_upload_prior": "Upload prior file (.prior)",
        "tl_upload_dataset": "Upload Dataset CSV",
        "tl_epochs": "Number of Epochs",
        "tl_batch": "Batch Size",
        "tl_val_split_toggle": "Use Validation Split",
        "tl_val_split_toggle_help": "Enable to split part of the dataset as validation data. Recommended for De Novo (Reinvent). Not required for LibInvent/LinkInvent.",
        "tl_val_split": "Validation Split Ratio",
        "tl_val_split_help": "Example: 0.20 means 20% of data is used for validation, 80% for training.",
        "tl_run_btn": "Run Transfer Learning",
        "tl_result_title": "Transfer Learning Complete!",
        "tl_download": "Download Finetuned Model (.prior)",

        # RL
        "rl_header": "Staged Learning (Reinforcement Learning)",
        "rl_prior_label": "Select Prior (Base Model)",
        "rl_agent_label": "Select Agent (TL Result / Base)",
        "rl_upload_custom": "Or upload your Prior (.prior)",
        "rl_upload_agent": "Or upload your Agent (.prior)",
        "rl_max_steps": "Max Steps",
        "rl_qed_weight": "QED Weight",
        "rl_mw_min": "Min Molecular Weight",
        "rl_mw_max": "Max Molecular Weight",
        "rl_run_btn": "Start Optimization (RL)",
        "rl_result_title": "Staged Learning (RL) Complete!",
        "rl_csv_wait": "Waiting for REINVENT to write CSV...",
        "rl_download": "Download RL Model (.prior)",

        # Sampling
        "samp_header": "Sampling",
        "samp_prior_label": "Select Prior",
        "samp_num_smiles": "Number of Molecules to Generate",
        "samp_run_btn": "Run Sampling",
        "samp_ref_smi": "Enter Reference SMILES (optional, to compute Tanimoto Similarity):",
        "samp_tanimoto_spin": "Computing Tanimoto Similarity...",
        "samp_result_metric_total": "Total Output",
        "samp_result_metric_valid": "Validity",
        "samp_result_metric_unique": "Uniqueness",
        "samp_eval_header": "Generation Metrics",
        "samp_download": "Download CSV",
        "samp_no_file": "Result file (sampling.csv) not yet available.",

        # Result viewer
        "result_close": "Close",
        "result_expander": "Show / Hide Results",
        "result_header": "Job Results",
        "tl_example_loaded": "Example data loaded.",
        "samp_example_loaded": "Example parameters loaded. Click Run Sampling.",
        "samp_header_title": "Sampling — Chemical Space Exploration",
        "samp_show_2d": "🔬 Show 2D Molecule Images (First 10)",
        "file_selected": "File selected",

        "api_http_error": "API server error {}: {}",

        "check_log": "Check run.log in the job folder.",

        "job_sent": "Job submitted!",

        "pre_max_mw_help": "Maximum molecular weight allowed (Daltons).",

        "pre_max_heavy_help": "Maximum number of heavy atoms.",

        "pre_min_heavy_help": "Minimum number of heavy (non-hydrogen) atoms in a molecule.",

        "rl_upload_custom": "Or upload your own Prior model (.prior)",

        "tl_preview_example": "Preview Example Data (first 5 rows)",

        "tl_download_example": "Download Example File (.csv)",

        "tl_example_active": "{} molecules loaded as example data — `{}`",

        "result_header": "Job Results",
        "tl_example_loaded": "Example data loaded.",
        "samp_example_loaded": "Example parameters loaded. Click Run Sampling.",
        "samp_header_title": "Sampling — Chemical Space Exploration",
        "samp_show_2d": "🔬 Show 2D Molecule Images (First 10)",
        "file_selected": "File selected",

        "api_http_error": "API server error {}: {}",

        "check_log": "Check run.log in the job folder.",

        "job_sent": "Job submitted!",

        "pre_max_mw_help": "Maximum molecular weight allowed (Daltons).",

        "pre_max_heavy_help": "Maximum number of heavy atoms.",

        "pre_min_heavy_help": "Minimum number of heavy (non-hydrogen) atoms in a molecule.",

        "rl_upload_custom": "Or upload your own Prior model (.prior)",

        "tl_preview_example": "Preview Example Data (first 5 rows)",

        "tl_download_example": "Download Example File (.csv)",

        "tl_example_active": "{} molecules loaded as example data — `{}`",


        "api_error": "Failed to contact API. Make sure the server is running.",

        "pre_sending": "Submitting preprocessing job...",

        "pre_no_file": "Please upload a CSV file first.",

        "pre_uncharge_help": "Normalize formal charges to neutral where possible.",

        "pre_uncharge": "Neutralize Charges (Uncharge)",

        "pre_stereo_help": "If checked, stereochemistry information (R/S) is preserved.",

        "pre_stereo": "Keep Stereochemistry",

        "pre_params": "Filter Parameters",

        "pre_upload": "Upload CSV file (must have a SMILES column)",

        "pre_upload_label": "Upload Dataset",

        "pre_info": "Filter and clean your SMILES dataset before Transfer Learning. Uses reinvent.datapipeline.",

        "api_conn_fail": "Failed to connect to API: {}",

        "tl_no_dataset": "Please upload a CSV dataset file or click 'Load Example Data' first.",

        "tl_val_split_help": "Example: 0.20 means 20% of data is used for validation, 80% for training.",

        "tl_val_split": "Validation Split Ratio",

        "tl_val_split_toggle_help": "Enable to split part of the dataset as validation data. Recommended for De Novo (Reinvent). Not required for LibInvent/LinkInvent.",

        "tl_val_split_toggle": "Use Validation Split",

        "tl_example_info": "The example file above will be used as dataset if you don't upload your own.",

        "tl_example_download_help": "Download this example file as a format reference",

        "tl_load_example_help": "Loads 30 drug-like molecules as a sample dataset",

        "tl_load_example": "Load Example Data",

        "tl_csv_hint": "CSV file must have a column named `SMILES`. Max 10 MB.",

        "tl_upload_dataset": "Upload Dataset CSV",

        "tl_upload_prior": "Upload Base Model (.prior / .pt / .ckpt)",

        "tl_custom_caption": "Upload a custom prior file as the starting point for fine-tuning.",

        "tl_tab_custom": "Upload Custom Base Model",

        "tl_tab_builtin": "Built-in Prior as Base",

        "tl_caption": "Fine-tune a prior model using your dataset. Output is a new `.prior` model ready for Sampling.",

        "samp_load_example_help": "Fills parameters with recommended values for a quick test run",

        "samp_load_example": "Load Example Parameters",

        "samp_upload_model_help": "If provided, this file takes priority over the built-in prior selection.",

        "samp_upload_model": "Upload model file",

        "samp_custom_caption": "Upload your own model file (from Transfer Learning, checkpoint, etc).",

        "samp_tab_custom": "Upload Custom Model (.prior / .pt / .ckpt)",

        "samp_tab_builtin": "Built-in Prior",

        "samp_caption": "Generate new molecules using a pre-trained prior or your custom checkpoint.",

        "rl_csv_wait": "Waiting for REINVENT to write CSV...",

        "rl_csv_cant_display": "CSV file found but cannot be displayed as a table.",

        "pre_download_info": "The downloaded .smi file can be used directly as a Transfer Learning dataset.",

        "pre_no_smi": "processed.smi file not found yet.",

        "pre_result_metric": "Valid Molecules After Filter",

        "samp_tanimoto_spin": "Computing Tanimoto Similarity...",

        "samp_ref_placeholder": "C1=CC=CC=C1",

        "samp_ref_smi": "Enter Reference SMILES (optional, to compute Tanimoto Similarity):",

        "samp_no_file": "Result file (sampling.csv) not yet available.",

        "api_error": "Failed to contact API. Make sure the server is running.",
        "job_not_found": "Job not found on server.",
    }
}


def t(key: str, lang: str = "id", *args) -> str:
    text = STRINGS.get(lang, STRINGS["id"]).get(key, key)
    if args:
        return text.format(*args)
    return text
