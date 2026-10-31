import os
import subprocess
import json
from datetime import datetime

JOBS_DIR = os.path.join(os.path.dirname(__file__), "jobs")

if not os.path.exists(JOBS_DIR):
    os.makedirs(JOBS_DIR)

def get_job_dir(job_id: str) -> str:
    return os.path.join(JOBS_DIR, job_id)

def init_job(job_id: str, mode: str):
    job_dir = get_job_dir(job_id)
    os.makedirs(job_dir, exist_ok=True)
    status_file = os.path.join(job_dir, "status.json")
    status_data = {
        "job_id": job_id,
        "mode": mode,
        "status": "QUEUED",
        "created_at": datetime.now().isoformat(),
        "finished_at": None,
        "error": None
    }
    with open(status_file, "w") as f:
        json.dump(status_data, f)
    return job_dir

def update_job_status(job_id: str, status: str, error: str = None):
    job_dir = get_job_dir(job_id)
    status_file = os.path.join(job_dir, "status.json")
    if os.path.exists(status_file):
        with open(status_file, "r") as f:
            data = json.load(f)
        data["status"] = status
        if status in ["COMPLETED", "FAILED"]:
            data["finished_at"] = datetime.now().isoformat()
        if error:
            data["error"] = error
        with open(status_file, "w") as f:
            json.dump(data, f)

def run_reinvent_job(job_id: str, toml_path: str):
    """
    Eksekutor background task untuk menjalankan subprocess REINVENT.
    """
    job_dir = get_job_dir(job_id)
    update_job_status(job_id, "RUNNING")
    
    log_path = os.path.join(job_dir, "run.log")
    
    # Path absolut menuju reinvent CLI yang ada di .venv
    reinvent_cli = r"D:\S2\REINVENT\REINVENT4-main\.venv\Scripts\reinvent.exe"
    
    try:
        with open(log_path, "w") as log_file:
            process = subprocess.Popen(
                [reinvent_cli, "-l", log_path, toml_path],
                cwd=job_dir,
                stdout=log_file,
                stderr=subprocess.STDOUT
            )
            process.wait()
            
        if process.returncode == 0:
            update_job_status(job_id, "COMPLETED")
        else:
            update_job_status(job_id, "FAILED", f"Proses exit dengan kode {process.returncode}. Cek run.log untuk detailnya.")
    except Exception as e:
        update_job_status(job_id, "FAILED", str(e))

def run_datapipeline_job(job_id: str, toml_path: str):
    job_dir = get_job_dir(job_id)
    update_job_status(job_id, "RUNNING")
    log_path = os.path.join(job_dir, "run.log")
    python_cli = r"D:\S2\REINVENT\REINVENT4-main\.venv\Scripts\python.exe"
    try:
        import subprocess
        with open(log_path, "w") as log_file:
            process = subprocess.Popen(
                [python_cli, "-m", "reinvent.datapipeline", "-l", log_path, toml_path],
                cwd=job_dir,
                stdout=log_file,
                stderr=subprocess.STDOUT
            )
            process.wait()
        if process.returncode == 0:
            update_job_status(job_id, "COMPLETED")
        else:
            update_job_status(job_id, "FAILED", f"Exit code {process.returncode}. Cek run.log")
    except Exception as e:
        update_job_status(job_id, "FAILED", str(e))
