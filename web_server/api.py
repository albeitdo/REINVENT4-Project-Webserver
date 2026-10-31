from fastapi import FastAPI, BackgroundTasks, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from typing import Optional
import os
import uuid
import json
import shutil

import toml_builder
import job_manager

app = FastAPI(title="REINVENT 4 Web API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ─────────────────────────── SAMPLING ───────────────────────────

@app.post("/api/sampling")
async def start_sampling(
    background_tasks: BackgroundTasks,
    prior_name: str = Form(...),
    num_smiles: int = Form(...),
    custom_prior: Optional[UploadFile] = File(None),
):
    job_id = str(uuid.uuid4())
    job_dir = job_manager.init_job(job_id, "sampling")

    # Pakai file upload custom jika ada, kalau tidak pakai alias/shorthand
    if custom_prior and custom_prior.filename:
        prior_path = os.path.join(job_dir, custom_prior.filename)
        with open(prior_path, "wb") as buffer:
            shutil.copyfileobj(custom_prior.file, buffer)
    else:
        prior_path = prior_name

    toml_path = toml_builder.create_sampling_toml(
        job_dir=job_dir,
        prior_file=prior_path,
        num_smiles=num_smiles,
        
    )

    background_tasks.add_task(job_manager.run_reinvent_job, job_id, toml_path)
    return {"job_id": job_id, "message": "Sampling job started in background."}


# ─────────────────────────── TRANSFER LEARNING ───────────────────────────

@app.post("/api/transfer_learning")
async def start_tl(
    background_tasks: BackgroundTasks,
    prior_name: str = Form(...),
    epochs: int = Form(...),
    batch_size: int = Form(...),
    val_split: float = Form(0.2),
    dataset_file: UploadFile = File(...),
    custom_prior: Optional[UploadFile] = File(None),
):
    job_id = str(uuid.uuid4())
    job_dir = job_manager.init_job(job_id, "transfer_learning")

    # Simpan dataset CSV
    input_csv = os.path.join(job_dir, "dataset.csv")
    with open(input_csv, "wb") as buffer:
        shutil.copyfileobj(dataset_file.file, buffer)

    # Pakai file upload custom prior jika ada
    if custom_prior and custom_prior.filename:
        prior_path = os.path.join(job_dir, custom_prior.filename)
        with open(prior_path, "wb") as buffer:
            shutil.copyfileobj(custom_prior.file, buffer)
    else:
        prior_path = prior_name

    import importlib
    importlib.reload(toml_builder)

    toml_path = toml_builder.create_transfer_learning_toml(
        job_dir=job_dir,
        prior_file=prior_path,
        input_csv=input_csv,
        epochs=epochs,
        batch_size=batch_size,
        val_split=val_split
    )

    background_tasks.add_task(job_manager.run_reinvent_job, job_id, toml_path)
    return {"job_id": job_id, "message": "Transfer Learning job started in background."}



# ─────────────────────── DATA PIPELINE ───────────────────────

@app.post("/api/preprocessing")
async def start_preprocessing(
    background_tasks: BackgroundTasks,
    dataset_file: UploadFile = File(...),
    min_heavy: int = Form(2),
    max_heavy: int = Form(90),
    max_mw: float = Form(1200.0),
    keep_stereo: bool = Form(True),
    uncharge: bool = Form(True),
):
    job_id = str(uuid.uuid4())
    job_dir = job_manager.init_job(job_id, "preprocessing")

    input_csv = os.path.join(job_dir, "dataset.csv")
    with open(input_csv, "wb") as buffer:
        import shutil
        shutil.copyfileobj(dataset_file.file, buffer)

    # Detect exact case of smiles column
    detected_smiles_col = "SMILES"
    try:
        with open(input_csv, "r", encoding="utf-8") as f:
            header = f.readline().strip()
            cols = [c.strip('"') for c in header.split(",")]
            for col in cols:
                if col.lower() == "smiles":
                    detected_smiles_col = col
                    break
    except Exception:
        pass

    elements = ["I", "O", "Cl", "N", "C", "F", "S", "Br"]

    toml_path = toml_builder.create_datapipeline_toml(
        job_dir=job_dir,
        input_csv=input_csv,
        elements=elements,
        min_heavy=min_heavy,
        max_heavy=max_heavy,
        max_mw=max_mw,
        keep_stereo=keep_stereo,
        uncharge=uncharge,
        smiles_column=detected_smiles_col
    )

    background_tasks.add_task(job_manager.run_datapipeline_job, job_id, toml_path)
    return {"job_id": job_id, "message": "Preprocessing job started in background."}


@app.get("/api/jobs/{job_id}/download_preprocessed")
async def download_preprocessed(job_id: str):
    job_dir = job_manager.get_job_dir(job_id)
    smi_path = os.path.join(job_dir, "processed.smi")
    if not os.path.exists(smi_path):
        raise HTTPException(status_code=404, detail="File hasil preprocessing belum tersedia.")
    return FileResponse(
        smi_path,
        media_type="text/plain",
        filename=f"processed_{job_id[:8]}.smi",
        headers={"Content-Disposition": f"attachment; filename=processed_{job_id[:8]}.smi"}
    )

# ─────────────────────────── JOB STATUS & DOWNLOAD ───────────────────────────

@app.get("/api/jobs/{job_id}")
async def get_job_status(job_id: str):
    job_dir = job_manager.get_job_dir(job_id)
    status_file = os.path.join(job_dir, "status.json")
    if not os.path.exists(status_file):
        raise HTTPException(status_code=404, detail="Job not found")
    with open(status_file, "r") as f:
        status_data = json.load(f)
    return status_data


@app.get("/api/jobs/{job_id}/download_model")
async def download_finetuned_model(job_id: str):
    """Endpoint untuk mengunduh model finetuned hasil Transfer Learning."""
    job_dir = job_manager.get_job_dir(job_id)
    model_path = os.path.join(job_dir, "finetuned.prior")
    if not os.path.exists(model_path):
        raise HTTPException(status_code=404, detail="File model belum tersedia atau job belum selesai.")
    return FileResponse(
        path=model_path,
        media_type="application/octet-stream",
        filename=f"finetuned_{job_id[:8]}.prior",
    )


@app.get("/api/jobs/{job_id}/download_results")
async def download_sampling_results(job_id: str):
    """Endpoint untuk mengunduh file CSV hasil sampling."""
    job_dir = job_manager.get_job_dir(job_id)
    csv_path = os.path.join(job_dir, "sampling.csv")
    if not os.path.exists(model_path):
        raise HTTPException(status_code=404, detail="File hasil sampling belum tersedia.")
    return FileResponse(
        path=csv_path,
        media_type="text/csv",
        filename=f"sampling_results_{job_id[:8]}.csv",
    )


#                                                        STAGED LEARNING (RL)                                                       

@app.post("/api/staged_learning")
async def start_staged_learning(
    background_tasks: BackgroundTasks,
    prior_name: str = Form(...),
    agent_name: str = Form(...),
    max_steps: int = Form(100),
    mw_min: float = Form(200.0),
    mw_max: float = Form(500.0),
    qed_weight: float = Form(1.0),
    custom_prior: Optional[UploadFile] = File(None),
    custom_agent: Optional[UploadFile] = File(None)
):
    job_id = str(uuid.uuid4())
    job_dir = job_manager.init_job(job_id, "staged_learning")
    
    repo_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "REINVENT4-main"))
    
    # Handle prior file
    if custom_prior:
        prior_file_path = os.path.join(job_dir, custom_prior.filename)
        with open(prior_file_path, "wb") as buffer:
            import shutil
            shutil.copyfileobj(custom_prior.file, buffer)
    else:
        prior_file_path = os.path.join(repo_dir, "priors", prior_name)
        if not os.path.exists(prior_file_path):
            raise HTTPException(status_code=400, detail=f"Prior {prior_name} tidak ditemukan.")
            
    # Handle agent file
    if custom_agent:
        agent_file_path = os.path.join(job_dir, custom_agent.filename)
        with open(agent_file_path, "wb") as buffer:
            import shutil
            shutil.copyfileobj(custom_agent.file, buffer)
    else:
        agent_file_path = os.path.join(repo_dir, "priors", agent_name)
        if not os.path.exists(agent_file_path):
            raise HTTPException(status_code=400, detail=f"Agent {agent_name} tidak ditemukan.")
            
    # Buat TOML
    toml_path = toml_builder.create_staged_learning_toml(
        job_dir=job_dir,
        prior_file=prior_file_path,
        agent_file=agent_file_path,
        max_steps=max_steps,
        mw_min=mw_min,
        mw_max=mw_max,
        qed_weight=qed_weight
    )
    
    # Jalankan REINVENT
    background_tasks.add_task(job_manager.run_reinvent_job, job_id, toml_path)
    return {"job_id": job_id, "message": "Staged Learning (RL) job started in background."}



@app.get("/api/jobs/{job_id}/download_rl")

async def download_rl_results(job_id: str):

    """Endpoint untuk mengunduh file CSV hasil RL."""

    job_dir = job_manager.get_job_dir(job_id)

    model_path = os.path.join(job_dir, "stage1.chkpt")

    if not os.path.exists(model_path):

        raise HTTPException(status_code=404, detail="File model hasil RL belum tersedia.")

        

    return FileResponse(

        csv_path,

        media_type="text/csv",

        filename=f"rl_results_{job_id[:8]}.csv",

        headers={"Content-Disposition": f"attachment; filename=rl_results_{job_id[:8]}.csv"}

    )

