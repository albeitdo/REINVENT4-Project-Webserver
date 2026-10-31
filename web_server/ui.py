import streamlit as st
import requests
import pandas as pd
import os
import json
from io import BytesIO
from rdkit import Chem
from rdkit.Chem import Draw, AllChem, DataStructs
from translations import t as _t

def t(key, *args):
    # Read directly from the sidebar/landing widget key if available
    # fallback to sidebar_lang, then lang_radio, then session_state["lang"], then "id"
    active_lang = "id"
    if "sidebar_lang" in st.session_state:
        active_lang = "id" if st.session_state["sidebar_lang"] == "Indonesia" else "en"
    elif "lang_radio" in st.session_state:
        active_lang = "id" if st.session_state["lang_radio"] == "Indonesia" else "en"
    else:
        active_lang = st.session_state.get("lang", "id")
    
    return _t(key, active_lang, *args)

import sys
import time
import subprocess

# Auto-start FastAPI backend server if running on cloud / background
def ensure_api_running():
    try:
        r = requests.get("http://localhost:8000/docs", timeout=0.8)
    except Exception:
        # Start uvicorn server in background
        web_dir = os.path.dirname(os.path.abspath(__file__))
        app_root = os.path.abspath(os.path.join(web_dir, ".."))
        reinvent_pkg = os.path.join(app_root, "REINVENT4-main")
        
        env = os.environ.copy()
        python_paths = [app_root, web_dir, reinvent_pkg]
        if "PYTHONPATH" in env:
            python_paths.append(env["PYTHONPATH"])
        env["PYTHONPATH"] = os.pathsep.join(python_paths)

        subprocess.Popen(
            [sys.executable, "-m", "uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"],
            cwd=web_dir,
            env=env,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        time.sleep(2.5)

ensure_api_running()

API_URL = "http://localhost:8000/api"
JOBS_DIR = os.path.join(os.path.dirname(__file__), "jobs")

st.set_page_config(page_title="REINVENT 4 Portal", layout="wide")

# ─────────────────────── Helpers ───────────────────────

def calc_tanimoto(smiles_list, ref_smiles):
    try:
        ref_mol = Chem.MolFromSmiles(ref_smiles)
        if ref_mol is None:
            return [None] * len(smiles_list)
        ref_fp = AllChem.GetMorganFingerprintAsBitVect(ref_mol, 2, nBits=2048)
        sims = []
        for smi in smiles_list:
            mol = Chem.MolFromSmiles(str(smi))
            if mol is None:
                sims.append(None)
            else:
                fp = AllChem.GetMorganFingerprintAsBitVect(mol, 2, nBits=2048)
                sims.append(round(DataStructs.TanimotoSimilarity(ref_fp, fp), 4))
        return sims
    except Exception:
        return [None] * len(smiles_list)

def render_sampling_results(job_id: str):
    job_dir = os.path.join(JOBS_DIR, job_id)
    csv_path = os.path.join(job_dir, "sampling.csv")

    if not os.path.exists(csv_path):
        st.warning(t("samp_no_file"))
        return

    df = pd.read_csv(csv_path)
    
    # --- EVALUASI METRIK ---
    total_smiles = len(df)
    valid_smiles = []
    for smi in df.get("SMILES", []):
        mol = Chem.MolFromSmiles(str(smi))
        if mol is not None:
            valid_smiles.append(Chem.MolToSmiles(mol))
            
    valid_count = len(valid_smiles)
    unique_count = len(set(valid_smiles))
    
    validity = (valid_count / total_smiles * 100) if total_smiles > 0 else 0
    uniqueness = (unique_count / valid_count * 100) if valid_count > 0 else 0
    
    st.markdown(f"### {t('samp_eval_header')}")
    m1, m2, m3 = st.columns(3)
    m1.metric(t("samp_result_metric_total"), f"{total_smiles} molekul")
    m2.metric(t("samp_result_metric_valid"), f"{validity:.1f}%", help="Persentase molekul yang valid secara struktur kimia.")
    m3.metric(t("samp_result_metric_unique"), f"{uniqueness:.1f}%", help="Persentase molekul unik dari total molekul yang valid.")
    st.divider()
    # -----------------------

    ref_smi = st.text_input(
        t("samp_ref_smi"),
        placeholder=t("samp_ref_placeholder"),
        key=f"ref_smi_{job_id}"
    )
    if ref_smi:
        with st.spinner(t("samp_tanimoto_spin")):
            if "SMILES" in df.columns:
                df["Tanimoto"] = calc_tanimoto(df["SMILES"].tolist(), ref_smi)

    st.dataframe(df, use_container_width=True)

    # Download CSV
    csv_bytes = df.to_csv(index=False).encode()
    st.download_button(
        f"⬇️ {t('samp_download')}",
        data=csv_bytes,
        file_name=f"sampling_{job_id[:8]}.csv",
        mime="text/csv",
    )

    # Render 2D grid
    if "SMILES" in df.columns and st.button(t("samp_show_2d"), key=f"render_{job_id}"):
        mols, legends = [], []
        for _, row in df.head(10).iterrows():
            mol = Chem.MolFromSmiles(str(row["SMILES"]))
            if mol:
                mols.append(mol)
                sim_txt = f"Sim: {row['Tanimoto']:.3f}" if "Tanimoto" in df.columns and pd.notnull(row.get("Tanimoto")) else ""
                legends.append(sim_txt)
        if mols:
            img = Draw.MolsToGridImage(mols, molsPerRow=5, subImgSize=(260, 260), legends=legends, returnPNG=False)
            st.image(img)

def render_preprocessing_results(job_id: str):
    import os
    job_dir = os.path.join(JOBS_DIR, job_id)
    smi_path = os.path.join(job_dir, "processed.smi")

    st.success(t("pre_result_title"))

    if os.path.exists(smi_path):
        with open(smi_path, "r", encoding="utf-8") as f:
            lines = [l.strip() for l in f if l.strip()]
        st.metric(t("pre_result_metric"), f"{len(lines)} SMILES")
        with st.expander(t("pre_result_preview")):
            st.code("\n".join(lines[:20]))
        
        # Sediakan download .smi dan .csv
        with open(smi_path, "rb") as f:
            smi_bytes = f.read()
            
        csv_text = "SMILES\n" + "\n".join(lines)
        csv_bytes = csv_text.encode("utf-8")
        
        dl_col1, dl_col2 = st.columns(2)
        with dl_col1:
            st.download_button(
                label="⬇️ Download CSV (.csv)",
                data=csv_bytes,
                file_name=f"processed_{job_id[:8]}.csv",
                mime="text/csv",
                key=f"dl_pre_csv_{job_id}",
                use_container_width=True
            )
        with dl_col2:
            st.download_button(
                label="⬇️ Download SMI (.smi)",
                data=smi_bytes,
                file_name=f"processed_{job_id[:8]}.smi",
                mime="text/plain",
                key=f"dl_pre_smi_{job_id}",
                use_container_width=True
            )
    else:
        st.warning(t("pre_no_smi"))

    st.info(t("pre_download_info"))

def render_tl_results(job_id: str):
    job_dir = os.path.join(JOBS_DIR, job_id)
    model_path = os.path.join(job_dir, "model.prior")
    if not os.path.exists(model_path):
        model_path = os.path.join(job_dir, "model_1.chkpt")
    
    st.success(t("tl_result_title"))
    if os.path.exists(model_path):
        with open(model_path, "rb") as f:
            model_bytes = f.read()
        st.download_button(
            label=f"⬇️ {t('tl_download')}",
            data=model_bytes,
            file_name=f"finetuned_{job_id[:8]}.prior",
            mime="application/octet-stream",
            key=f"dl_tl_{job_id}"
        )
    else:
        st.warning(t("tl_csv_wait") if "tl_csv_wait" in STRINGS.get("id", {}) else "Model belum tersedia.")

def render_rl_results(job_id: str):
    job_dir = os.path.join(JOBS_DIR, job_id)
    csv_path = os.path.join(job_dir, "staged_learning_1.csv")
    model_path = os.path.join(job_dir, "stage1.chkpt")
    
    st.success(t("rl_result_title"))
    
    if os.path.exists(csv_path):
        try:
            df = pd.read_csv(csv_path)
            st.dataframe(df, use_container_width=True)
        except Exception:
            st.info(t("rl_csv_cant_display"))
    else:
        st.warning(t("rl_csv_wait"))
        
    if os.path.exists(model_path):
        with open(model_path, "rb") as f:
            model_bytes = f.read()
        st.download_button(
            label=f"⬇️ {t('rl_download')}",
            data=model_bytes,
            file_name=f"rl_model_{job_id[:8]}.prior",
            mime="application/octet-stream",
            key=f"dl_rl_{job_id}"
        )

# ─────────────────────── Landing Page ───────────────────────

if "app_entered" not in st.session_state:
    st.session_state["app_entered"] = False

if not st.session_state["app_entered"]:
    st.markdown("""
    <style>
        .landing-title {
            font-size: 3rem;
            font-weight: 800;
            color: #1B3A6B;
            text-align: center;
            margin-top: 3rem;
            letter-spacing: 1px;
        }
        .landing-subtitle {
            font-size: 1.15rem;
            color: #444;
            text-align: center;
            max-width: 700px;
            margin: 0.5rem auto 2.5rem auto;
            line-height: 1.7;
        }
        .feature-card {
            background: #EEF2F7;
            border-left: 4px solid #1B3A6B;
            border-radius: 6px;
            padding: 1rem 1.2rem;
            margin-bottom: 0.75rem;
        }
        .feature-title {
            font-weight: 700;
            color: #1B3A6B;
            font-size: 1rem;
            margin-bottom: 0.2rem;
        }
        .feature-desc {
            color: #555;
            font-size: 0.9rem;
        }
        .divider-line {
            border: none;
            border-top: 1px solid #dce3ef;
            margin: 2rem auto;
            max-width: 600px;
        }
    </style>
    """, unsafe_allow_html=True)



    st.markdown(f'<div class="landing-title">{t("landing_title")}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="landing-subtitle">{t("landing_subtitle")}</div>', unsafe_allow_html=True)

    st.markdown("<hr class='divider-line'>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"""
        <div class="feature-card">
            <div class="feature-title">{t("feat_preprocessing")}</div>
            <div class="feature-desc">{t("feat_preprocessing_desc")}</div>
        </div>
        <div class="feature-card">
            <div class="feature-title">{t("feat_tl")}</div>
            <div class="feature-desc">{t("feat_tl_desc")}</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="feature-card">
            <div class="feature-title">{t("feat_rl")}</div>
            <div class="feature-desc">{t("feat_rl_desc")}</div>
        </div>
        <div class="feature-card">
            <div class="feature-title">{t("feat_sampling")}</div>
            <div class="feature-desc">{t("feat_sampling_desc")}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<hr class='divider-line'>", unsafe_allow_html=True)

    lang_col1, lang_col2, lang_col3 = st.columns([2, 2, 2])
    with lang_col2:
        lang_choice = st.radio(
            "Bahasa / Language",
            ["Indonesia", "English"],
            horizontal=True,
            key="lang_radio",
            label_visibility="collapsed"
        )
        st.session_state["lang"] = "id" if lang_choice == "Indonesia" else "en"

    col_btn = st.columns([2, 2, 2])
    with col_btn[1]:
        if st.button(t("enter_btn"), type="primary", use_container_width=True):
            st.session_state["app_entered"] = True
            st.rerun()
    st.stop()

# ─────────────────────── Sidebar ───────────────────────

st.sidebar.title("REINVENT 4 Portal")
_lang_disp = "Indonesia" if st.session_state.get("lang", "id") == "id" else "English"
_lang_sel = st.sidebar.radio("Bahasa / Language", ["Indonesia", "English"], index=0 if _lang_disp=="Indonesia" else 1, horizontal=True, label_visibility="collapsed", key="sidebar_lang")
st.session_state["lang"] = "id" if _lang_sel == "Indonesia" else "en"
mode = st.sidebar.radio(
    t("sidebar_mode_label"),
    [t("mode_preprocessing"), t("mode_tl"), t("mode_rl"), t("mode_sampling")]
)
st.sidebar.divider()

# ─────────────────────── SAMPLING ───────────────────────

PRIOR_BUILTIN = {
    "De Novo — reinvent (.reinvent)": ".reinvent",
    "Scaffold/R-group — libinvent (.libinvent)": ".libinvent",
    "Linker Design — linkinvent (.linkinvent)": ".linkinvent",
}

SAMPLES_DIR = os.path.join(os.path.dirname(__file__), "samples")
SAMPLE_TL_CSV = os.path.join(SAMPLES_DIR, "sample_tl_dataset.csv")

if mode == "Sampling":
    st.header(t("samp_header_title"))
    st.caption(t("samp_caption"))

    tab_builtin, tab_custom = st.tabs([t("samp_tab_builtin"), t("samp_tab_custom")])

    with tab_builtin:
        prior_builtin_choice = st.selectbox(t("samp_prior_label"), list(PRIOR_BUILTIN.keys()))

    with tab_custom:
        st.caption(t("samp_custom_caption"))
        sampling_custom_file = st.file_uploader(
            t("samp_upload_model"),
            type=["prior", "pt", "ckpt"],
            help=t("samp_upload_model_help"),
            key="sampling_custom_prior_uploader"
        )
        if sampling_custom_file:
            st.success(f"{t('file_selected')}: `{sampling_custom_file.name}` ({round(sampling_custom_file.size/1024, 1)} KB)")

    st.divider()

    ex_col, _ = st.columns([1, 3])
    with ex_col:
        if st.button(t("samp_load_example"), help=t("samp_load_example_help")):
            st.session_state["s_num"] = 20
            st.session_state["s_batch"] = 20
            st.toast(t("samp_example_loaded"))

    num_smiles = st.number_input(t("samp_num_smiles"), min_value=1, max_value=10000, value=st.session_state.get("s_num", 50), key="s_num")

    if st.button(t("samp_run_btn"), type="primary"):
        use_custom = sampling_custom_file is not None
        prior_name = PRIOR_BUILTIN[prior_builtin_choice]
        data = {
            "prior_name": "__custom__" if use_custom else prior_name,
            "num_smiles": num_smiles,
        }
        files = None
        if use_custom:
            files = {"custom_prior": (sampling_custom_file.name, sampling_custom_file.getvalue(), "application/octet-stream")}

        try:
            res = requests.post(f"{API_URL}/sampling", data=data, files=files)
            if res.status_code == 200:
                job_id = res.json()["job_id"]
                st.session_state["current_job"] = job_id
                st.session_state["current_job_mode"] = "sampling"
                label = sampling_custom_file.name if use_custom else prior_name
                st.success(f"{t('job_sent')} ID: `{job_id[:8]}` | Model: `{label}`")
            else:
                st.error(f"{t('api_http_error', res.status_code, res.text)}")
        except requests.exceptions.ConnectionError:
            st.error(t("api_error"))

# ─────────────────────── TRANSFER LEARNING ───────────────────────

elif mode == t("mode_tl"):
    st.header(t("tl_header"))
    st.caption(t("tl_caption"))

    tab_tl_builtin, tab_tl_custom = st.tabs([t("tl_tab_builtin"), t("tl_tab_custom")])

    with tab_tl_builtin:
        tl_prior_choice = st.selectbox(t("tl_prior_label"), list(PRIOR_BUILTIN.keys()))

    with tab_tl_custom:
        st.caption(t("tl_custom_caption"))
        tl_custom_prior = st.file_uploader(
            t("tl_upload_prior"),
            type=["prior", "pt", "ckpt"],
            key="tl_custom_prior_uploader"
        )
        if tl_custom_prior:
            st.success(f"{t('file_selected')}: `{tl_custom_prior.name}` ({round(tl_custom_prior.size/1024, 1)} KB)")

    st.divider()

    ds_label_col, ds_btn_col = st.columns([3, 1])
    with ds_label_col:
        st.markdown(f"**{t('tl_upload_dataset')}**")
        st.caption(t("tl_csv_hint"))
    with ds_btn_col:
        st.markdown("&nbsp;", unsafe_allow_html=True)
        load_example = st.button(t("tl_load_example"), help=t("tl_load_example_help"))

    if load_example:
        with open(SAMPLE_TL_CSV, "rb") as f:
            st.session_state["tl_example_bytes"] = f.read()
        st.session_state["tl_example_name"] = "sample_tl_dataset.csv"
        st.toast(t("tl_example_loaded"))

    if "tl_example_bytes" in st.session_state:
        import io
        example_df = pd.read_csv(io.BytesIO(st.session_state["tl_example_bytes"]))
        st.success(f"{t('tl_example_active', len(example_df), st.session_state['tl_example_name'])}")
        with st.expander(t("tl_preview_example")):
            st.dataframe(example_df.head(5), use_container_width=True)
        st.download_button(
            t("tl_download_example"),
            data=st.session_state["tl_example_bytes"],
            file_name="sample_tl_dataset.csv",
            mime="text/csv",
            help=t("tl_example_download_help")
        )
        st.info(t("tl_example_info"))

    dataset_file = st.file_uploader(
        t("tl_upload_dataset"),
        type=["csv", "smi", "txt"],
        help="Mendukung file CSV (kolom SMILES), atau file SMILES baris demi baris (.smi / .txt)",
        key="tl_dataset_uploader"
    )

    col1, col2 = st.columns(2)
    with col1:
        epochs = st.number_input(t("tl_epochs"), min_value=1, value=10, key="tl_epoch")
    with col2:
        batch_size = st.number_input(t("tl_batch"), min_value=1, value=64, key="tl_batch")

    use_split = st.checkbox(
        t("tl_val_split_toggle"),
        value=True,
        help=t("tl_val_split_toggle_help")
    )
    val_split = 0.0
    if use_split:
        val_split = st.slider(
            t("tl_val_split"),
            min_value=0.05, max_value=0.5, value=0.2, step=0.05,
            help=t("tl_val_split_help")
        )

    if st.button(t("tl_run_btn"), type="primary"):
        active_dataset_bytes = None
        active_dataset_name = None
        if dataset_file is not None:
            active_dataset_bytes = dataset_file.getvalue()
            active_dataset_name = dataset_file.name
        elif "tl_example_bytes" in st.session_state:
            active_dataset_bytes = st.session_state["tl_example_bytes"]
            active_dataset_name = st.session_state["tl_example_name"]

        if active_dataset_bytes is None:
            st.error(t("tl_no_dataset"))
        else:
            use_custom_prior = tl_custom_prior is not None
            prior_name = PRIOR_BUILTIN[tl_prior_choice]
            data = {
                "prior_name": "__custom__" if use_custom_prior else prior_name,
                "epochs": epochs,
                "batch_size": batch_size,
            "val_split": val_split,
            }
            files = {"dataset_file": (active_dataset_name, active_dataset_bytes, "text/csv")}
            if use_custom_prior:
                files["custom_prior"] = (tl_custom_prior.name, tl_custom_prior.getvalue(), "application/octet-stream")
            try:
                res = requests.post(f"{API_URL}/transfer_learning", data=data, files=files)
                if res.status_code == 200:
                    job_id = res.json()["job_id"]
                    st.session_state["current_job"] = job_id
                    st.session_state["current_job_mode"] = "transfer_learning"
                    st.success(f"{t('job_sent')} ID: `{job_id[:8]}` | Dataset: `{active_dataset_name}`")
                else:
                    st.error(f"{t('api_http_error', res.status_code, res.text)}")
            except requests.exceptions.ConnectionError:
                st.error(t("api_error"))

# ─────────────────────── STAGED LEARNING (RL) ───────────────────────

elif mode == t("mode_rl"):
    st.header(t("rl_header"))
    
    c_p, c_a = st.columns(2)
    with c_p:
        rl_prior_choice = st.selectbox(t("rl_prior_label"), list(PRIOR_BUILTIN.keys()), key="rl_prior")
        rl_custom_prior = st.file_uploader(t("rl_upload_custom"), type=["prior"], key="rl_custom_p")
    with c_a:
        rl_agent_choice = st.selectbox(t("rl_agent_label"), list(PRIOR_BUILTIN.keys()), key="rl_agent")
        rl_custom_agent = st.file_uploader(t("rl_upload_agent"), type=["prior"], key="rl_custom_a")
    
    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        rl_max_steps = st.number_input(t("rl_max_steps"), min_value=10, value=100, step=10)
        rl_qed = st.slider(t("rl_qed_weight"), min_value=0.0, max_value=10.0, value=1.0, step=0.1)
    with col2:
        rl_mw_min = st.number_input(t("rl_mw_min"), value=250.0)
        rl_mw_max = st.number_input(t("rl_mw_max"), value=450.0)
        
    if st.button(t("rl_run_btn"), type="primary"):
        use_custom_prior = rl_custom_prior is not None
        use_custom_agent = rl_custom_agent is not None
        prior_name = PRIOR_BUILTIN[rl_prior_choice]
        agent_name = PRIOR_BUILTIN[rl_agent_choice]
        
        data = {
            "prior_name": "__custom__" if use_custom_prior else prior_name,
            "agent_name": "__custom__" if use_custom_agent else agent_name,
            "max_steps": rl_max_steps,
            "mw_min": rl_mw_min,
            "mw_max": rl_mw_max,
            "qed_weight": rl_qed
        }
        
        files = {}
        if use_custom_prior:
            files["custom_prior"] = (rl_custom_prior.name, rl_custom_prior.getvalue(), "application/octet-stream")
        if use_custom_agent:
            files["custom_agent"] = (rl_custom_agent.name, rl_custom_agent.getvalue(), "application/octet-stream")
            
        try:
            res = requests.post(f"{API_URL}/staged_learning", data=data, files=files if files else None)
            if res.status_code == 200:
                job_id = res.json()["job_id"]
                st.session_state["current_job"] = job_id
                st.session_state["current_job_mode"] = "staged_learning"
                st.success(f"{t('job_sent')} ID: `{job_id[:8]}`")
            else:
                st.error(f"Error: {res.text}")
        except Exception as e:
            st.error(t("api_conn_fail", e))


# ─────────────────────── PREPROCESSING ───────────────────────

if mode == t("mode_preprocessing"):
    st.header(t("pre_header"))
    st.info(t("pre_info"))

    st.subheader(t("pre_upload_label"))
    pre_file = st.file_uploader(t("pre_upload"), type=["csv"], key="pre_file")

    st.subheader(t("pre_params"))
    col1, col2 = st.columns(2)
    with col1:
        min_heavy = st.number_input(t("pre_min_heavy"), min_value=1, max_value=50, value=2, help=t("pre_min_heavy_help"))
        max_heavy = st.number_input(t("pre_max_heavy"), min_value=10, max_value=300, value=90, help=t("pre_max_heavy_help"))
    with col2:
        max_mw = st.number_input(t("pre_max_mw"), min_value=100.0, max_value=5000.0, value=1200.0, help=t("pre_max_mw_help"))
        keep_stereo = st.checkbox(t("pre_stereo"), value=True, help=t("pre_stereo_help"))

    uncharge = st.checkbox(t("pre_uncharge"), value=True, help=t("pre_uncharge_help"))

    if st.button(t("pre_run_btn"), type="primary"):
        if pre_file is None:
            st.error(t("pre_no_file"))
        else:
            with st.spinner(t("pre_sending")):
                try:
                    files = {"dataset_file": (pre_file.name, pre_file.getvalue(), "text/csv")}
                    data = {
                        "min_heavy": min_heavy,
                        "max_heavy": max_heavy,
                        "max_mw": max_mw,
                        "keep_stereo": keep_stereo,
                        "uncharge": uncharge,
                    }
                    res = requests.post(f"{API_URL}/preprocessing", data=data, files=files)
                    if res.status_code == 200:
                        resp = res.json()
                        st.session_state["current_job"] = resp["job_id"]
                        st.session_state["current_job_mode"] = "preprocessing"
                        st.success(f"{t('pre_started', resp['job_id'][:8])}")
                    else:
                        st.error(f"Error: {res.text}")
                except Exception as e:
                    st.error(t("api_conn_fail", e))

# ─────────────────────── Sidebar: Job Tracker ───────────────────────

st.sidebar.subheader(t("sidebar_live_status"))
if "current_job" in st.session_state:
    job_id = st.session_state["current_job"]
    job_mode = st.session_state.get("current_job_mode", "sampling")
    st.sidebar.caption(f"Job ID: `{job_id[:8]}...`")

    try:
        status_res = requests.get(f"{API_URL}/jobs/{job_id}")
        if status_res.status_code == 200:
            status_data = status_res.json()
            status = status_data["status"]

            if status == "QUEUED":
                st.sidebar.info(t("status_queued"))
            elif status == "RUNNING":
                st.sidebar.warning(t("status_running"))
                if st.sidebar.button(t("btn_refresh")):
                    st.rerun()
            elif status == "COMPLETED":
                st.sidebar.success(t("status_completed"))
                if st.sidebar.button(t("btn_view")):
                    st.session_state["view_job"] = job_id
                    st.session_state["view_job_mode"] = job_mode
            elif status == "FAILED":
                st.sidebar.error(t("status_failed"))
                err_msg = status_data.get("error", t("check_log"))
                st.sidebar.error(err_msg)
                
                # Show run.log if available
                log_file = os.path.join(JOBS_DIR, job_id, "run.log")
                if os.path.exists(log_file):
                    try:
                        with open(log_file, "r", encoding="utf-8", errors="ignore") as lf:
                            log_content = lf.read()
                        with st.sidebar.expander("📄 Detail run.log"):
                            st.code(log_content[-2000:], language="text")
                    except Exception:
                        pass
        else:
            st.sidebar.warning(t("job_not_found"))
    except Exception:
        st.sidebar.error(t("api_error"))
else:
    st.sidebar.caption(t("no_active_job"))

# ─────────────────────── Riwayat Job (History) ───────────────────────

st.sidebar.divider()
st.sidebar.subheader(t("sidebar_history"))

def get_job_history():
    jobs = []
    if os.path.exists(JOBS_DIR):
        for d in os.listdir(JOBS_DIR):
            status_path = os.path.join(JOBS_DIR, d, "status.json")
            if os.path.exists(status_path):
                try:
                    with open(status_path, "r") as f:
                        jobs.append(json.load(f))
                except Exception:
                    pass
    jobs.sort(key=lambda x: x.get("created_at", ""), reverse=True)
    return jobs

history = get_job_history()
if not history:
    st.sidebar.caption(t("no_history"))
else:
    history_container = st.sidebar.container(height=320, border=True)
    with history_container:
        for job in history:
            jid = job.get("job_id", "")
            jmode = job.get("mode", "unknown").upper()
            jstat = job.get("status", "unknown")
            
            icon = "⏳"
            if jstat == "COMPLETED": icon = "✅"
            elif jstat == "FAILED": icon = "❌"
            elif jstat == "QUEUED": icon = "🕐"
            
            st.markdown(f"**{jmode}**<br>`{jid[:8]}`", unsafe_allow_html=True)
            st.caption(f"{icon} {jstat}")
            
            if jstat == "COMPLETED":
                if st.button(t("btn_view"), key=f"hist_{jid}"):
                    st.session_state["view_job"] = jid
                    st.session_state["view_job_mode"] = job.get("mode", "sampling")
                    st.rerun()
            elif jstat == "FAILED":
                err_text = job.get("error", "")
                if err_text:
                    st.caption(f":red[{err_text}]")
                hist_log = os.path.join(JOBS_DIR, jid, "run.log")
                if os.path.exists(hist_log):
                    with st.expander("Detail Log"):
                        try:
                            with open(hist_log, "r", encoding="utf-8", errors="ignore") as hf:
                                st.code(hf.read()[-1500:], language="text")
                        except Exception:
                            pass
            st.markdown("---")

# ─────────────────────── Result Viewer ───────────────────────

if st.session_state.get("view_job"):
    st.divider()
    view_job_id = st.session_state["view_job"]
    view_mode = st.session_state.get("view_job_mode", "sampling")

    header_col, close_col = st.columns([8, 1])
    with header_col:
        st.subheader(f"{t('result_header')} `{view_job_id[:8]}` ({view_mode.replace('_', ' ').title()})")
    with close_col:
        if st.button(t("result_close"), key="close_result"):
            del st.session_state["view_job"]
            st.session_state.pop("view_job_mode", None)
            st.rerun()

    with st.expander(t("result_expander"), expanded=True):
        if view_mode == "sampling":
            render_sampling_results(view_job_id)
        elif view_mode == "transfer_learning":
            render_tl_results(view_job_id)
        elif view_mode == "staged_learning":
            render_rl_results(view_job_id)
        elif view_mode == "preprocessing":
            render_preprocessing_results(view_job_id)

