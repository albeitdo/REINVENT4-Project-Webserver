import toml
import os

def create_sampling_toml(job_dir: str, prior_file: str, num_smiles: int):
    """
    Membuat file konfigurasi sampling.toml untuk REINVENT 4.
    """
    config = {
        "run_type": "sampling",
        "device": "cpu",  # Memastikan pakai CPU karena setup kita saat ini CPU
        "tb_logdir": "tb_logs",
        "json_out_config": "_sampling.json",
        "parameters": {
            "model_file": prior_file,
            "output_file": "sampling.csv",
            "num_smiles": num_smiles,
            
            "unique_molecules": True,
                    }
    }
    
    toml_path = os.path.join(job_dir, "sampling.toml")
    with open(toml_path, "w") as f:
        toml.dump(config, f)
        
    return toml_path

def create_transfer_learning_toml(job_dir: str, prior_file: str, input_csv: str, epochs: int, batch_size: int, val_split: float = 0.2):
    """
    Membuat file konfigurasi transfer_learning.toml untuk REINVENT 4.
    Mengkonversi CSV ke .smi terlebih dahulu sesuai format yang dibutuhkan.
    """
    import csv

    import random
    
    train_smi_path = os.path.join(job_dir, "train.smi")
    valid_smi_path = os.path.join(job_dir, "valid.smi")
    
    smiles_list = []
    # Check if file has CSV header with SMILES or is a plain list of SMILES
    with open(input_csv, "r", encoding="utf-8", errors="ignore") as f:
        first_line = f.readline().strip()
        f.seek(0)
        
        # If header has comma or smiles keyword, try DictReader
        if "," in first_line or "smiles" in first_line.lower():
            try:
                reader = csv.DictReader(f)
                smiles_col = None
                if reader.fieldnames:
                    for col in reader.fieldnames:
                        if col and col.strip().upper() == "SMILES":
                            smiles_col = col
                            break
                if smiles_col:
                    for row in reader:
                        smi = (row.get(smiles_col) or "").strip()
                        if smi:
                            smiles_list.append(smi)
            except Exception:
                pass

        # If not parsed as CSV or empty, treat as line-by-line SMILES file (.smi / .txt)
        if not smiles_list:
            f.seek(0)
            for line in f:
                line_str = line.strip()
                if not line_str or line_str.startswith("#"):
                    continue
                # Split by space or tab if line has id (standard .smi format: SMILES ID)
                parts = line_str.split()
                if parts and parts[0].lower() != "smiles":
                    smiles_list.append(parts[0])

    if not smiles_list:
        raise ValueError("Tidak ada struktur SMILES yang valid ditemukan dalam dataset.")
            
    random.shuffle(smiles_list)
    
    if val_split > 0.0:
        split_idx = int(len(smiles_list) * (1.0 - val_split))
        train_smiles = smiles_list[:split_idx]
        valid_smiles = smiles_list[split_idx:] if split_idx < len(smiles_list) else smiles_list
    else:
        # Tidak ada split — pakai semua data untuk training, validasi pakai file yang sama
        train_smiles = smiles_list
        valid_smiles = smiles_list
        
    with open(train_smi_path, "w", encoding="utf-8") as f:
        for smi in train_smiles:
            f.write(smi + "\n")
    with open(valid_smi_path, "w", encoding="utf-8") as f:
        for smi in valid_smiles:
            f.write(smi + "\n")

    num_refs = min(100, batch_size)

    config = {
        "run_type": "transfer_learning",
        "device": "cpu",
        "tb_logdir": "tb_TL",
        "json_out_config": "_tl.json",
        "parameters": {
            "num_epochs": epochs,
            "batch_size": batch_size,
            "save_every_n_epochs": max(1, epochs),
            "num_refs": num_refs,
            "sample_batch_size": 100,
            "tb_isim": False,
            "input_model_file": prior_file,
            "smiles_file": train_smi_path,
            "output_model_file": "finetuned.prior",
            "validation_smiles_file": valid_smi_path,
        }
    }

    toml_path = os.path.join(job_dir, "tl.toml")
    with open(toml_path, "w") as f:
        toml.dump(config, f)

    return toml_path

def create_staged_learning_toml(job_dir: str, prior_file: str, agent_file: str, max_steps: int, mw_min: float, mw_max: float, qed_weight: float):
    config = {
        "run_type": "staged_learning",
        "device": "cpu",
        "tb_logdir": "tb_logs",
        "json_out_config": "_staged_learning.json",
        "parameters": {
            "summary_csv_prefix": "staged_learning",
            "use_checkpoint": False,
            "purge_memories": False,
            "prior_file": prior_file,
            "agent_file": agent_file,
            "batch_size": 32
                            },
        "learning_strategy": {
            "type": "dap",
            "sigma": 128,
            "rate": 0.0001
        },
        "stage": [
            {
                "chkpt_file": "stage1.chkpt",
                "termination": "simple",
                "max_score": 0.99,
                "min_steps": min(25, max_steps),
                "max_steps": max_steps,
                "scoring": {
                    "type": "geometric_mean",
                    "component": []
                }
            }
        ]
    }
    
    components = []
    
    components.append({
        "MolecularWeight": {
            "endpoint": [{
                "name": "Molecular weight",
                "weight": 1.0,
                "transform": {
                    "type": "double_sigmoid",
                    "high": mw_max,
                    "low": mw_min,
                    "coef_div": mw_max,
                    "coef_si": 20.0,
                    "coef_se": 20.0
                }
            }]
        }
    })
    
    if qed_weight > 0:
        components.append({
            "QED": {
                "endpoint": [{
                    "name": "QED",
                    "weight": qed_weight
                }]
            }
        })
        
    config["stage"][0]["scoring"]["component"] = components

    toml_path = os.path.join(job_dir, "rl.toml")
    with open(toml_path, "w") as f:
        toml.dump(config, f)
        
    return toml_path

def create_datapipeline_toml(job_dir: str, input_csv: str, elements: list, min_heavy: int, max_heavy: int, max_mw: float, keep_stereo: bool, uncharge: bool, smiles_column: str = "SMILES"):
    import toml
    import os
    config = {
        "input_csv_file": input_csv,
        "smiles_column": smiles_column,
        "separator": ",",
        "output_smiles_file": "processed.smi",
        "num_procs": 1,
        "chunk_size": 500,
        "filter": {
            "elements": elements,
            "transforms": ["standard"],
            "min_heavy_atoms": min_heavy,
            "max_heavy_atoms": max_heavy,
            "max_mol_weight": max_mw,
            "keep_stereo": keep_stereo,
            "keep_isotope_molecules": True,
            "uncharge": uncharge,
            "kekulize": False,
            "randomize_smiles": False,
            "report_errors": False
        }
    }
    toml_path = os.path.join(job_dir, "datapipeline.toml")
    with open(toml_path, "w") as f:
        toml.dump(config, f)
    return toml_path
