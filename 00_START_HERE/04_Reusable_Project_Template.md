# 04 — Reusable Project Template

> **Copy this folder for every new project. It is your starting point.**

---

## 🎯 Why A Template?

Every research project has the **same shape**:

```
data/  notebooks/  src/  experiments/  results/  docs/  references/  reports/
```

If you start from this template, you skip the "where do I put my code?" question forever.

---

## 📦 What's In The Template

```
00_Project_Template/
├── README.md                ← project overview
├── requirements.txt         ← Python dependencies
├── .gitignore               ← files Git should ignore
├── configs/                 ← YAML configs for experiments
├── data/                    ← datasets (raw, interim, processed, external)
│   ├── raw/
│   ├── interim/
│   ├── processed/
│   └── external/
├── notebooks/               ← Jupyter exploration
├── src/                     ← reusable Python code
│   ├── data/                ← loaders, cleaning
│   ├── features/            ← feature engineering
│   ├── models/              ← model definitions
│   ├── evaluation/          ← metrics, plots
│   └── utils/               ← helpers
├── experiments/             ← training scripts
├── results/                 ← outputs
│   ├── figures/
│   ├── tables/
│   └── logs/
├── docs/                    ← notes, design docs
├── references/              ← papers.bib
└── reports/                 ← final paper, slides
```

---

## 🚀 How To Use It

### Step 1: Copy the template

```bash
# Pick a name for your project (lowercase, dashes, no spaces)
PROJECT_NAME="my-thesis-on-fake-news"

# Copy the template
cp -r 00_Project_Template/ ~/projects/$PROJECT_NAME/
cd ~/projects/$PROJECT_NAME

# Initialize Git
git init
git add .
git commit -m "Initial project skeleton from research-foundation template"
```

### Step 2: Customize the README

Open `README.md` and fill in:

```markdown
# [Your Project Title]

> One-sentence summary.

## 🎯 Research Question
- Q1: ...
- Q2: ...

## 📊 Dataset
- Name, source, size, license

## 🛠️ Method
- Baseline 1, Baseline 2, Proposed method

## 📈 Results
| Method | Metric 1 | Metric 2 |
|---|---|---|
| Baseline 1 | ... | ... |
| Proposed | ... | ... |

## 🚀 How To Run
```bash
pip install -r requirements.txt
python experiments/train.py --config configs/main.yaml
```
```

### Step 3: Add your data

```bash
# Put raw data in data/raw/
cp /path/to/dataset.csv data/raw/

# Don't commit large data to Git (use DVC or external storage)
```

### Step 4: Start a notebook

```bash
jupyter notebook notebooks/01-eda.ipynb
```

### Step 5: Add a config

```yaml
# configs/exp001.yaml
experiment_name: "exp001_baseline_rf"
seed: 42
data:
  path: data/processed/features.parquet
model:
  type: random_forest
  params:
    n_estimators: 200
    max_depth: 10
training:
  test_size: 0.2
  cv_folds: 5
```

### Step 6: Run an experiment

```bash
python experiments/train.py --config configs/exp001.yaml
```

---

## 📁 The `src/` Layout — Why?

Each subfolder has **one job**:

| Folder | Job | Examples |
|---|---|---|
| `src/data/` | Load + clean | `load_data.py`, `clean.py` |
| `src/features/` | Build features | `build_features.py`, `encode.py` |
| `src/models/` | Define + train | `train.py`, `model.py` |
| `src/evaluation/` | Measure + plot | `metrics.py`, `plots.py` |
| `src/utils/` | Helpers | `io.py`, `seed.py` |

This is the **Cookiecutter Data Science** layout (the most common in industry and academia). Once you learn it, every project feels the same.

---

## 🧪 Naming Conventions

Use these so your project is consistent:

| Thing | Convention | Example |
|---|---|---|
| Folders | lowercase + underscore | `data/`, `src/models/` |
| Notebooks | `NN-purpose.ipynb` | `01-eda.ipynb`, `02-baseline.ipynb` |
| Configs | `NN-name.yaml` | `01-baseline.yaml`, `02-tuning.yaml` |
| Python files | lowercase + underscore | `train_model.py` |
| Functions | lowercase + underscore | `def load_data():` |
| Classes | PascalCase | `class DataLoader:` |
| Constants | UPPERCASE | `SEED = 42` |

---

## 📋 What Goes Where? (decision tree)

```
Is it data?
  → data/raw/  (raw, untouched)
  → data/processed/  (cleaned, model-ready)
  → data/external/  (third-party)
  → data/interim/  (in-progress)

Is it code?
  → src/  (reusable, importable)
  → notebooks/  (exploratory, narrative)
  → experiments/  (one-off runs, scripts)

Is it output?
  → results/figures/  (PNG, PDF)
  → results/tables/  (CSV, LaTeX)
  → results/logs/  (training logs, MLflow)

Is it documentation?
  → docs/  (design notes, decisions)
  → references/  (papers.bib, PDFs)
  → reports/  (final paper, slides, poster)
```

---

## 🔒 What NOT To Commit

Already in `.gitignore`:

- `__pycache__/`, `*.pyc`
- `.env` (API keys!)
- `data/raw/` (large files)
- `*.log`
- `.ipynb_checkpoints/`
- Virtual envs (`venv/`, `env/`)
- ML model weights > 100MB (use Git LFS or DVC)

For large data, use:
- **DVC** (data version control) — `dvc add data/raw/`
- **Hugging Face Datasets** — for NLP/CV
- **External storage** (S3, university drive)

---

## 🔁 Reuse Across Projects

| When You Start A New Project | Action |
|---|---|
| Topic picked, advisor confirmed | `cp -r 00_Project_Template/ new-project/` |
| Old project ended | Archive it; don't delete |
| Adding a new experiment | Add a new YAML in `configs/` and a new script in `experiments/` |
| Want to share code between projects | Move it to a small Python package, install with `pip install -e .` |

---

## ✅ Done When

- [ ] You copied the template for a sample project
- [ ] You filled in the README
- [ ] You added a `.gitignore` (already in template)
- [ ] You created your first config file
- [ ] You ran your first experiment
- [ ] You pushed to GitHub

Now return to `00_START_HERE/01_How_To_Use_This_Repo.md` and pick a folder to work on next.
