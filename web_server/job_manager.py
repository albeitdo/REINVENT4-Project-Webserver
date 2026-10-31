import os
import sys
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

def get_python_exe() -> str:
    # Menggunakan sys.executable (kompatibel Windows & Linux Cloud)
    return sys.executable

def run_reinvent_job(job_id: str, toml_path: str):
    """
    Eksekutor background task untuk menjalankan subprocess REINVENT.
    """
    job_dir = get_job_dir(job_id)
    update_job_status(job_id, "RUNNING")
    
    log_path = os.path.join(job_dir, "run.log")
    python_cli = get_python_exe()
    
    # Siapkan environment agar REINVENT menemukan modul dan folder priors
    web_dir = os.path.dirname(os.path.abspath(__file__))
    app_root = os.path.abspath(os.path.join(web_dir, ".."))
    reinvent_pkg = os.path.join(app_root, "REINVENT4-main")
    priors_dir = os.path.join(reinvent_pkg, "priors")
    
    env = os.environ.copy()
    env["REINVENT_PRIOR_BASE"] = priors_dir
    python_paths = [app_root, web_dir, reinvent_pkg]
    if "PYTHONPATH" in env:
        python_paths.append(env["PYTHONPATH"])
    env["PYTHONPATH"] = os.pathsep.join(python_paths)

    try:
        with open(log_path, "w") as log_file:
            process = subprocess.Popen(
                [python_cli, "-m", "reinvent", "-l", log_path, toml_path],
                cwd=job_dir,
                env=env,
                stdout=log_file,
                stderr=subprocess.STDOUT
            )
            process.wait()
            
        if process.returncode == 0:
            update_job_status(job_id, "COMPLETED")
        else:
            err_snippet = ""
            if os.path.exists(log_path):
                try:
                    with open(log_path, "r", encoding="utf-8", errors="ignore") as lf:
                        lines = [line.strip() for line in lf.readlines() if line.strip()]
                        err_snippet = " | ".join(lines[-3:]) if lines else ""
                except Exception:
                    pass
            msg = f"Exit code {process.returncode}."
            if err_snippet:
                msg += f" Error: {err_snippet}"
            else:
                msg += " Cek run.log"
            update_job_status(job_id, "FAILED", msg)
    except Exception as e:
        update_job_status(job_id, "FAILED", str(e))

def run_datapipeline_job(job_id: str, toml_path: str):
    job_dir = get_job_dir(job_id)
    update_job_status(job_id, "RUNNING")
    log_path = os.path.join(job_dir, "run.log")
    python_cli = get_python_exe()
    web_dir = os.path.dirname(os.path.abspath(__file__))
    app_root = os.path.abspath(os.path.join(web_dir, ".."))
    reinvent_pkg = os.path.join(app_root, "REINVENT4-main")
    env = os.environ.copy()
    python_paths = [app_root, web_dir, reinvent_pkg]
    if "PYTHONPATH" in env:
        python_paths.append(env["PYTHONPATH"])
    env["PYTHONPATH"] = os.pathsep.join(python_paths)

    try:
        with open(log_path, "w") as log_file:
            process = subprocess.Popen(
                [python_cli, "-m", "reinvent.datapipeline", "-l", log_path, toml_path],
                cwd=job_dir,
                env=env,
                stdout=log_file,
                stderr=subprocess.STDOUT
            )
            process.wait()
        if process.returncode == 0:
            update_job_status(job_id, "COMPLETED")
        else:
            err_snippet = ""
            if os.path.exists(log_path):
                try:
                    with open(log_path, "r", encoding="utf-8", errors="ignore") as lf:
                        lines = [line.strip() for line in lf.readlines() if line.strip()]
                        err_snippet = " | ".join(lines[-3:]) if lines else ""
                except Exception:
                    pass
            msg = f"Exit code {process.returncode}."
            if err_snippet:
                msg += f" Error: {err_snippet}"
            else:
                msg += " Cek run.log"
            update_job_status(job_id, "FAILED", msg)
    except Exception as e:
        update_job_status(job_id, "FAILED", str(e))
