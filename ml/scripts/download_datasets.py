import os
import subprocess
import sys

def install_and_import(package):
    try:
        import datasets
    except ImportError:
        print(f"Installing {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    finally:
        globals()[package] = __import__(package)

print("Preparing to download datasets via HuggingFace (no authentication required)...")
install_and_import("datasets")

raw_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'raw'))
os.makedirs(raw_dir, exist_ok=True)

# Define HF dataset paths
hf_datasets = {
    "NSL-KDD": "dvilasuero/NSL-KDD",
    "CICIDS-2017": "dvilasuero/CICIDS2017",
    "UNSW-NB15": "dvilasuero/UNSW-NB15",
    "BETH": "joshb/beth_dataset" # Example alternative if available
}

for name, repo in hf_datasets.items():
    print(f"\n[{name}] Downloading from HuggingFace ({repo})...")
    try:
        # Load dataset
        ds = datasets.load_dataset(repo)
        
        # Save each split to CSV
        dataset_dir = os.path.join(raw_dir, name)
        os.makedirs(dataset_dir, exist_ok=True)
        
        for split in ds.keys():
            csv_path = os.path.join(dataset_dir, f"{split}.csv")
            print(f"  -> Saving {split} split to {csv_path}...")
            ds[split].to_csv(csv_path, index=False)
            
        print(f"✅ {name} successfully downloaded and saved.")
    except Exception as e:
        print(f"❌ Failed to download {name}: {e}")
        print("Note: If a dataset is missing from HF, it requires manual download via Kaggle/UNB.")

print("\n🎉 Download process finished.")
