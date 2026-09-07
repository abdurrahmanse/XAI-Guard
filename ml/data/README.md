# XAI-Guard Data Directory

This directory contains the entire data pipeline lifecycle. 
**DO NOT COMMIT DATA FILES TO GIT.** They are managed by DVC.

## Directory Structure
- `raw/{dataset_name}/`: Original, immutable data downloaded from sources.
- `interim/{dataset_name}/`: Data after initial cleaning and standardisation.
- `processed/{dataset_name}/`: Data after feature encoding and scaling.
- `features/`: Engineered features (e.g., temporal windows).
- `selected/`: Data after feature selection (e.g., top 20 features).
- `splits/{train,val,test}/`: Final data splits ready for model training.

## Accessing Data
To download or restore the data locally, simply run:
```bash
dvc pull
```
