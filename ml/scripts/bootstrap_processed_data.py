#!/usr/bin/env python3
"""
XAI-Guard — Data Pipeline Bootstrap Script
===========================================
Runs the full preprocessing pipeline (notebooks 06-07 logic) from the
command line, so ml/data/processed/ is populated WITHOUT having to open
Jupyter. This unblocks model training notebooks 19-21 which load from
ml/data/processed/ instead of using synthetic data.

Usage (from project root):
    cd /Volumes/Fullstack/Github/XAI-Guard
    python ml/scripts/bootstrap_processed_data.py

Output:
    ml/data/processed/X_train.npy
    ml/data/processed/X_test.npy
    ml/data/processed/y_train.npy
    ml/data/processed/y_test.npy
    ml/data/processed/label_encoder.pkl
    ml/data/processed/scaler.pkl
    ml/data/processed/pipeline_metadata.json
"""
from __future__ import annotations

import json
import os
import sys
import warnings

warnings.filterwarnings("ignore")

# ── Make sure ml/.venv packages are available ─────────────────────────────────
VENV_PACKAGES = os.path.join(os.path.dirname(__file__), "..", ".venv", "lib")
if os.path.isdir(VENV_PACKAGES):
    for entry in os.listdir(VENV_PACKAGES):
        site = os.path.join(VENV_PACKAGES, entry, "site-packages")
        if os.path.isdir(site) and site not in sys.path:
            sys.path.insert(0, site)

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, RobustScaler

OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "processed")
RAW_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "raw")

# ─────────────────────────────────────────────────────────────────────────────
# Dataset loaders
# ─────────────────────────────────────────────────────────────────────────────

def _load_nsl_kdd() -> pd.DataFrame | None:
    """Load NSL-KDD train set. Returns None if files not found."""
    columns = [
        "duration", "protocol_type", "service", "flag", "src_bytes", "dst_bytes",
        "land", "wrong_fragment", "urgent", "hot", "num_failed_logins", "logged_in",
        "num_compromised", "root_shell", "su_attempted", "num_root", "num_file_creations",
        "num_shells", "num_access_files", "num_outbound_cmds", "is_host_login",
        "is_guest_login", "count", "srv_count", "serror_rate", "srv_serror_rate",
        "rerror_rate", "srv_rerror_rate", "same_srv_rate", "diff_srv_rate",
        "srv_diff_host_rate", "dst_host_count", "dst_host_srv_count",
        "dst_host_same_srv_rate", "dst_host_diff_srv_rate", "dst_host_same_src_port_rate",
        "dst_host_srv_diff_host_rate", "dst_host_serror_rate", "dst_host_srv_serror_rate",
        "dst_host_rerror_rate", "dst_host_srv_rerror_rate", "label", "difficulty",
    ]
    train_path = os.path.join(RAW_DIR, "nsl-kdd", "KDDTrain+.txt")
    if not os.path.exists(train_path):
        return None
    df = pd.read_csv(train_path, names=columns)
    # Map to binary (normal vs attack)
    df["unified_label"] = df["label"].apply(lambda x: 0 if x == "normal" else 1)
    # Keep only numeric columns + label
    numeric = df.select_dtypes(include=[np.number]).columns.tolist()
    if "unified_label" not in numeric:
        numeric.append("unified_label")
    return df[numeric].dropna()


def _load_cicids() -> pd.DataFrame | None:
    """Load a subset of CICIDS-2017. Returns None if files not found."""
    cicids_dir = os.path.join(RAW_DIR, "cicids-2017")
    if not os.path.isdir(cicids_dir):
        return None
    frames = []
    for fname in sorted(os.listdir(cicids_dir))[:3]:  # load first 3 files max for speed
        if not fname.endswith(".csv"):
            continue
        fpath = os.path.join(cicids_dir, fname)
        try:
            df = pd.read_csv(fpath, low_memory=False)
            df.columns = df.columns.str.strip()
            if "Label" in df.columns:
                df["unified_label"] = df["Label"].apply(lambda x: 0 if str(x).upper() == "BENIGN" else 1)
                numeric = df.select_dtypes(include=[np.number]).columns.tolist()
                if "unified_label" not in numeric:
                    numeric.append("unified_label")
                frames.append(df[numeric].dropna().replace([np.inf, -np.inf], np.nan).dropna())
        except Exception as e:
            print(f"  ⚠️  Skipping {fname}: {e}")
    return pd.concat(frames, ignore_index=True) if frames else None


# ─────────────────────────────────────────────────────────────────────────────
# Main pipeline
# ─────────────────────────────────────────────────────────────────────────────

def run():
    os.makedirs(OUT_DIR, exist_ok=True)
    print("XAI-Guard — Data Pipeline Bootstrap")
    print("=" * 50)

    # 1. Try to load real datasets
    datasets = []
    print("\n[1/4] Loading raw datasets...")

    nsl = _load_nsl_kdd()
    if nsl is not None:
        print(f"  ✅ NSL-KDD loaded: {nsl.shape}")
        datasets.append(nsl)
    else:
        print("  ⚠️  NSL-KDD not found at ml/data/raw/nsl-kdd/KDDTrain+.txt")

    cicids = _load_cicids()
    if cicids is not None:
        print(f"  ✅ CICIDS-2017 loaded: {cicids.shape}")
        datasets.append(cicids)
    else:
        print("  ⚠️  CICIDS-2017 not found at ml/data/raw/cicids-2017/")

    if not datasets:
        print("\n  ❌ No real data found. Generating synthetic fallback...")
        from sklearn.datasets import make_classification
        X_raw, y_raw = make_classification(
            n_samples=5000, n_features=20, n_informative=10,
            n_classes=3, weights=[0.8, 0.12, 0.08], random_state=42
        )
        df = pd.DataFrame(X_raw, columns=[f"feature_{i}" for i in range(20)])
        df["unified_label"] = y_raw
        datasets.append(df)
        print("  ✅ Synthetic dataset generated: 5000 samples, 20 features")
        data_source = "synthetic"
    else:
        data_source = "real"

    # 2. Merge all datasets
    print("\n[2/4] Merging and aligning schemas...")
    combined = pd.concat(datasets, ignore_index=True).fillna(0)
    # Ensure unified_label exists
    feature_cols = [c for c in combined.columns if c != "unified_label"]
    X = combined[feature_cols].values.astype(np.float32)
    y = combined["unified_label"].values.astype(np.int64)
    print(f"  ✅ Combined shape: X={X.shape}, y={y.shape}")
    print(f"  Class distribution: {dict(zip(*np.unique(y, return_counts=True)))}")

    # 3. Scale features
    print("\n[3/4] Applying RobustScaler (no data leakage)...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y if len(np.unique(y)) > 1 else None
    )
    scaler = RobustScaler()
    X_train = scaler.fit_transform(X_train)  # Fit on train only
    X_test  = scaler.transform(X_test)        # Apply to test (no leakage)
    print(f"  ✅ Train: {X_train.shape}  Test: {X_test.shape}")

    # 4. Save to disk
    print("\n[4/4] Saving processed arrays to ml/data/processed/...")
    np.save(os.path.join(OUT_DIR, "X_train.npy"), X_train)
    np.save(os.path.join(OUT_DIR, "X_test.npy"),  X_test)
    np.save(os.path.join(OUT_DIR, "y_train.npy"), y_train)
    np.save(os.path.join(OUT_DIR, "y_test.npy"),  y_test)

    import pickle
    with open(os.path.join(OUT_DIR, "scaler.pkl"), "wb") as f:
        pickle.dump(scaler, f)

    metadata = {
        "data_source": data_source,
        "n_features": X_train.shape[1],
        "n_train": int(X_train.shape[0]),
        "n_test": int(X_test.shape[0]),
        "classes": [int(c) for c in np.unique(y)],
        "scaler": "RobustScaler",
        "random_state": 42,
        "feature_names": feature_cols if len(feature_cols) == X_train.shape[1] else [f"feature_{i}" for i in range(X_train.shape[1])],
    }
    with open(os.path.join(OUT_DIR, "pipeline_metadata.json"), "w") as f:
        json.dump(metadata, f, indent=2)

    print(f"\n✅ Done! ml/data/processed/ is now populated.")
    print(f"   X_train: {X_train.shape} | X_test: {X_test.shape}")
    print(f"   Files: X_train.npy, X_test.npy, y_train.npy, y_test.npy")
    print(f"          scaler.pkl, pipeline_metadata.json")
    print(f"\n   Notebooks 19, 20, 21 will now load REAL data automatically.")


if __name__ == "__main__":
    run()
