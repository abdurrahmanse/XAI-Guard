# RESEARCH_PROCESS.md — The End-to-End Research Workflow

> **The single most important file in this repo. Read it top to bottom. It walks you through every stage of doing Data Science research, from "I have no idea" to "I have a published paper."**

---

## 🗺️ The Full Map (read in order)

| Stage | What Happens | Folder |
|---|---|---|
| 0. Mindset | What research really is | `00_START_HERE/02` |
| 1. Idea | Find a question | `01_Research_Basics/03`, `05` |
| 2. Literature | Read what others did | `01_Research_Basics/02`, `06_Paper_And_Publishing/02` |
| 3. Setup | Tools, project folder, advisor | `00_START_HERE/04`, `03_Tools/` |
| 4. Data | Find, clean, explore | `04_Data_Work/01-03` |
| 5. Baseline | Build a simple model first | `05_Machine_Learning/01` |
| 6. Method | Build your proposed model | `05_Machine_Learning/02-08` |
| 7. Experiments | Train, tune, ablate | `05_Machine_Learning/03,09-10` |
| 8. Evaluation | Metrics, plots, statistical tests | `05_Machine_Learning/03`, `02_Math_And_Stats/03` |
| 9. Documentation | Reproducibility, README, code | `05_Machine_Learning/11`, `06_Paper_And_Publishing/07` |
| 10. Writing | Paper, IMRaD | `06_Paper_And_Publishing/01` |
| 11. Publishing | arXiv, journal, conference | `06_Paper_And_Publishing/03-04` |
| 12. Presentation | Slides, poster, talk | `06_Paper_And_Publishing/06` |
| 13. Thesis | Tie everything together | `07_My_Thesis/` |

Each stage below has: **what to do**, **why it matters**, **the theory in 3 lines**, **the code**, and **the next step**.

---

## Stage 0 — Mindset: What Is Research?

**The 3-line theory:**
Research = finding answers to questions nobody has answered. In Data Science, that means proposing a method, running controlled experiments, and reporting the result honestly. School work has known answers; research has none — that's the whole point.

**Why it matters:**
If you don't know what research is, you'll write a school project and call it a thesis. The difference is **novelty + soundness + honesty**.

**Action:** Read `00_START_HERE/02_What_Is_Research.md`.

---

## Stage 1 — Idea Generation

**The 3-line theory:**
Good research questions come from (a) gaps in the literature, (b) real problems you care about, and (c) data you can actually access. Combine all three. The "gap" is what no one has done yet — that's your contribution.

**Methods (pick 3, do all 10):**

1. **Read 30 papers** in your area. Write a 1-line summary of each.
2. **Look at "Future Work" sections** — those are the open questions.
3. **Brainstorm 10 ideas** in 30 minutes, no filter.
4. **Filter by data:** can you actually get the data?
5. **Filter by scope:** can you finish in 3-6 months?
6. **Filter by advisor:** will someone supervise this?
7. **Combine 2 ideas** that haven't been combined.
8. **Apply method X to domain Y** where X and Y are well-known but never crossed.
9. **Look at what fails** in current papers — improve it.
10. **Ask practitioners** (doctors, bankers, teachers) what their problems are.

**Code (sketch):** Keep an `ideas.md` file:

```markdown
# Topic Ideas (ranked)
1. [Score 9/10] Fake news detection with transformers on FakeNewsNet
   Gap: existing work uses BERT but not domain-adapted
   Data: ✅ public, Code: ✅ public, Time: ✅ 4 months
2. [Score 7/10] ...
```

**Next:** Talk to 3 professors. See `06_Paper_And_Publishing/08_Reaching_Out_To_Professors.md`.

---

## Stage 2 — Literature Review

**The 3-line theory:**
A literature review is a *map* of what exists. You read 30-100 papers, group them by theme, build a comparison table, and end with "the gap" — what's missing. Your thesis should fill that gap.

**Steps:**

1. **Define keywords** — `"deep learning" AND "medical imaging" AND "X-ray"`
2. **Search 4 databases** — Google Scholar, arXiv, PubMed, IEEE Xplore
3. **Filter by year** — last 3-5 years (older only for foundational papers)
4. **Use the 3-pass method** for each (see `01_Research_Basics/02`)
5. **Take notes in a spreadsheet:**

| Paper | Year | Method | Dataset | Metric | Limitation |
|---|---|---|---|---|---|
| Smith | 2023 | BERT | FakeNewsNet | F1=0.85 | no domain adapt |

6. **Group by theme**, not by author
7. **Build a comparison table** of methods
8. **End with the gap** (1 sentence)

**Code:** Use Zotero to manage PDFs + a Google Sheet for the table.

**Theory frame:** Use the **PRISMA** flow (Identification → Screening → Eligibility → Included) for a systematic review.

**Next:** Write a 1-page problem statement.

---

## Stage 3 — Project Setup

**The 3-line theory:**
A research project without structure wastes time. Set up folders, version control, environments, and an experiment tracker on day 1. Future you will thank you.

**Code:**

```bash
# 1. Copy the project template
cp -r 00_Project_Template/ ~/projects/my-thesis/
cd ~/projects/my-thesis

# 2. Create a virtual environment
python -m venv venv
source venv/bin/activate   # Mac/Linux
# venv\Scripts\activate    # Windows

# 3. Install minimal dependencies
pip install numpy pandas scikit-learn matplotlib seaborn

# 4. Save them
pip freeze > requirements.txt

# 5. Initialize Git
git init
git add .
git commit -m "Initial project skeleton"
git branch -M main
git remote add origin https://github.com/you/my-thesis.git
git push -u origin main

# 6. Open in VSCode
code .
```

**Folder layout** (already in template):

```
data/{raw,interim,processed,external}/
notebooks/   ← exploration
src/{data,features,models,evaluation,utils}/
experiments/ ← runnable training scripts
results/{figures,tables,logs}/
configs/     ← YAML configs (one per experiment)
docs/        ← design notes
references/  ← papers.bib
reports/     ← paper, slides
```

**Tools to set up once:**

- ✅ Python + venv
- ✅ Git + GitHub
- ✅ VSCode or Jupyter
- ✅ LaTeX (Overleaf account)
- ✅ Zotero (reference manager)
- ✅ MLflow or W&B (experiment tracking)
- ✅ DVC (data versioning, optional)

**Next:** Find and load your data.

---

## Stage 4 — Data Work

**The 3-line theory:**
Data is the foundation. Most research time is spent here, not on models. "Garbage in, garbage out" is real. The 3 jobs: **clean** the data, **understand** the data, **prepare** the data.

**Code (end-to-end mini-pipeline):**

```python
# src/data/load.py
import pandas as pd
from pathlib import Path

def load_raw(name: str) -> pd.DataFrame:
    """Load a raw dataset by name."""
    path = Path("data/raw") / f"{name}.csv"
    df = pd.read_csv(path)
    print(f"Loaded {name}: {df.shape}")
    return df

# src/data/clean.py
def basic_clean(df: pd.DataFrame) -> pd.DataFrame:
    """Drop duplicates, fix dtypes, basic NA handling."""
    df = df.drop_duplicates()
    # Example: fill numeric NA with median, categorical with mode
    for col in df.select_dtypes(include="number"):
        df[col] = df[col].fillna(df[col].median())
    for col in df.select_dtypes(include="object"):
        df[col] = df[col].fillna(df[col].mode()[0])
    return df

# src/features/split.py
from sklearn.model_selection import train_test_split

def split_features_target(df, target, test_size=0.2, seed=42):
    X = df.drop(columns=[target])
    y = df[target]
    return train_test_split(X, y, test_size=test_size,
                            random_state=seed, stratify=y)
```

**Always do (the EDA loop):**

```python
print(df.shape); print(df.dtypes); print(df.isnull().sum())
print(df.describe())
df.hist(figsize=(12,10)); plt.show()
sns.heatmap(df.corr(), annot=True); plt.show()
```

**Theory (data leakage):** If information from the test set leaks into training, your results are fake. Common causes: scaling before splitting, target encoding with test rows, dropping NAs using global stats. **Always split first, then fit transformers on train only.**

```python
# CORRECT (no leakage)
from sklearn.pipeline import Pipeline
pipe = Pipeline([("scaler", StandardScaler()), ("clf", LogisticRegression())])
pipe.fit(X_train, y_train)
pipe.score(X_test, y_test)
```

**Next:** Build a baseline.

---

## Stage 5 — Baseline

**The 3-line theory:**
A baseline is the simplest thing that could possibly work. You need it to know whether your fancy method is actually better. Without a baseline, you can't say "my model is good" — only "my model is something."

**Code:**

```python
# experiments/01_baseline.py
import pandas as pd
from sklearn.model_selection import cross_val_score
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

# Load
df = pd.read_csv("data/processed/clean.csv")
X = df.drop(columns=["target"])
y = df["target"]

# Baselines (3 minimum)
models = {
    "most_frequent":  DummyClassifier(strategy="most_frequent"),
    "logistic_reg":   LogisticRegression(max_iter=1000),
    "random_forest":  RandomForestClassifier(n_estimators=200, random_state=42),
}

for name, model in models.items():
    scores = cross_val_score(model, X, y, cv=5, scoring="f1_macro")
    print(f"{name:15s} F1 = {scores.mean():.3f} ± {scores.std():.3f}")
```

**Expected output:**
```
most_frequent   F1 = 0.250 ± 0.005
logistic_reg    F1 = 0.781 ± 0.020
random_forest   F1 = 0.842 ± 0.015
```

**Rule:** Your proposed method must beat the strongest baseline by a meaningful margin (and the improvement must be statistically significant).

**Next:** Build your proposed method.

---

## Stage 6 — Method (The Proposed Approach)

**The 3-line theory:**
Your proposed method is the **new thing** in your thesis. It can be: (a) a new architecture, (b) a new combination of existing methods, (c) a new training procedure, (d) a new application of X to Y. The simplest innovation is fine — most MSc theses are (b) or (d).

**Code template (PyTorch):**

```python
# src/models/proposed.py
import torch
import torch.nn as nn

class ProposedModel(nn.Module):
    def __init__(self, in_dim, hidden=128, out_dim=2, dropout=0.3):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(in_dim, hidden), nn.ReLU(), nn.Dropout(dropout),
            nn.Linear(hidden, hidden), nn.ReLU(), nn.Dropout(dropout),
            nn.Linear(hidden, out_dim),
        )
    def forward(self, x): return self.net(x)

# src/models/train.py
def train_one_epoch(model, loader, opt, criterion, device):
    model.train()
    total, correct, loss_sum = 0, 0, 0
    for x, y in loader:
        x, y = x.to(device), y.to(device)
        opt.zero_grad()
        out = model(x)
        loss = criterion(out, y)
        loss.backward()
        opt.step()
        loss_sum += loss.item() * x.size(0)
        correct += (out.argmax(1) == y).sum().item()
        total += x.size(0)
    return loss_sum / total, correct / total
```

**Theory (what makes it "yours"):** Write a 3-sentence summary that a non-expert can understand:
> "We propose a [model name] that combines [A] with [B] to solve [problem]. The key idea is [one sentence]. We evaluate on [dataset] and beat [baseline] by [X%]."

**Next:** Run experiments systematically.

---

## Stage 7 — Experiments (The Fun Part)

**The 3-line theory:**
Experiments answer "does my method work, how well, and why?" You do 3 types: (1) **main results** vs baselines, (2) **ablations** to find which design choice matters, (3) **analysis** (error analysis, failure cases, fairness).

**Experiment tracking (MLflow):**

```python
import mlflow
mlflow.set_experiment("my-thesis")

with mlflow.start_run(run_name="proposed_v1"):
    mlflow.log_param("lr", 0.001)
    mlflow.log_param("batch_size", 32)
    mlflow.log_param("seed", 42)
    # ... train ...
    mlflow.log_metric("f1", 0.89)
    mlflow.log_artifact("results/figures/confusion.png")
```

**Configs (YAML):**

```yaml
# configs/proposed_v1.yaml
experiment: proposed_v1
seed: 42
data:
  path: data/processed/features.parquet
model:
  type: proposed
  hidden: 128
  dropout: 0.3
training:
  lr: 0.001
  epochs: 20
  batch_size: 32
```

**Ablations:** Change one thing at a time.

| Variant | What Changed | F1 |
|---|---|---|
| Baseline RF | — | 0.842 |
| Proposed (full) | + our additions | 0.891 |
| Proposed − A | remove component A | 0.872 |
| Proposed − B | remove component B | 0.880 |
| Proposed − A − B | remove both | 0.860 |

**Statistical significance:** Run with 5+ random seeds. Use paired t-test (see `02_Math_And_Stats/03`).

**Next:** Evaluate properly.

---

## Stage 8 — Evaluation

**The 3-line theory:**
Evaluation answers "is the result real, big, and important?" Use the right metric, the right test, and visualize the result. Never rely on a single number.

**Theory (metric choice):**

| Task | Use |
|---|---|
| Balanced binary classification | Accuracy, F1 |
| Imbalanced | F1, PR-AUC, MCC |
| Multi-class | Macro-F1 |
| Regression | MAE, RMSE, R² |
| Ranking | NDCG, MAP |
| Generation | BLEU, ROUGE, BERTScore |

**Code (full evaluation):**

```python
# src/evaluation/metrics.py
from sklearn.metrics import (accuracy_score, f1_score, classification_report,
                              confusion_matrix, roc_auc_score)
import seaborn as sns, matplotlib.pyplot as plt

def evaluate(y_true, y_pred, y_prob=None, name="model"):
    print(f"=== {name} ===")
    print(f"Accuracy: {accuracy_score(y_true, y_pred):.3f}")
    print(f"F1 (macro): {f1_score(y_true, y_pred, average='macro'):.3f}")
    if y_prob is not None:
        print(f"AUC: {roc_auc_score(y_true, y_prob):.3f}")
    print(classification_report(y_true, y_pred, digits=3))
    cm = confusion_matrix(y_true, y_pred)
    sns.heatmap(cm, annot=True, fmt="d"); plt.title(name); plt.show()
```

**Statistical test (is the improvement real?):**

```python
from scipy import stats
# Suppose you ran 5 seeds: scores_A and scores_B
t, p = stats.ttest_rel(scores_A, scores_B)
print(f"p = {p:.4f}")  # If p < 0.05, B is significantly better than A
```

**Visualizations (always include):**

- Confusion matrix (classification)
- Predicted vs actual (regression)
- Learning curves (loss over epochs)
- Bar chart comparing methods
- Ablation chart
- One attention or feature-importance plot

**Next:** Document for reproducibility.

---

## Stage 9 — Documentation & Reproducibility

**The 3-line theory:**
Reproducibility = someone else can run your code and get the same numbers. Without it, reviewers reject. Set seeds, fix versions, log configs, release code.

**Code (set seed everywhere):**

```python
# src/utils/seed.py
import random, numpy as np, torch
def set_seed(seed: int = 42):
    random.seed(seed); np.random.seed(seed)
    torch.manual_seed(seed); torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False
```

**Documentation checklist:**

- [ ] `README.md` with: what, how to install, how to run
- [ ] `requirements.txt` (or `environment.yml`)
- [ ] `data/README.md` — where the data is, how to get it
- [ ] `configs/` — every experiment is a YAML
- [ ] `results/` — every run has a log + figures
- [ ] `paper.pdf` — final paper
- [ ] License (MIT, Apache 2.0, etc.)

**Release:** Push to GitHub, tag a release, optionally make a Docker image.

**Next:** Write the paper.

---

## Stage 10 — Writing The Paper (IMRaD)

**The 3-line theory:**
Papers follow IMRaD: **Introduction, Methods, Results, Discussion**. Each section has one job. A reader should be able to understand your contribution in 10 minutes by reading intro + figures + conclusion.

**Structure (with target lengths for an 8-page paper):**

| Section | Pages | Job |
|---|---|---|
| Title | 0.1 | What + key result |
| Abstract | 0.3 | 5 sentences: problem, gap, method, result, conclusion |
| Introduction | 1.5 | Why, what, gap, your contribution |
| Related Work | 1.0 | How your work fits the field |
| Methods | 2.0 | What you did, with enough detail to reproduce |
| Experiments | 2.0 | Setup, baselines, main results, ablations |
| Discussion | 0.5 | Strengths, limitations, future work |
| Conclusion | 0.3 | One paragraph |
| References | 1.0 | All papers you cited |

**The "So What?" test:** For every paragraph, ask "so what?" If you can't answer, cut it.

**The figure checklist:**

- [ ] At least 1 figure per section
- [ ] Every figure has a caption that stands alone
- [ ] All figures referenced in text as "Figure 1 shows..."
- [ ] Figures are vector (PDF) or high-DPI (PNG ≥ 300 dpi)

**Writing tips:**

- Short sentences (< 25 words)
- Active voice ("We trained..." not "A model was trained...")
- One idea per paragraph
- Read it out loud — if you stumble, rewrite

**Next:** Submit.

---

## Stage 11 — Publishing

**The 3-line theory:**
Publishing = sharing your work. Start with arXiv (free, instant), then conferences (fast, peer review), then journals (slow, detailed). Pick venues that read your kind of paper.

**Steps:**

1. **arXiv first** — always. Pre-print, gets a DOI, citable.
2. **Pick 3 target venues** — see `06_Paper_And_Publishing/03`.
3. **Match the template** — IEEE, ACM, NeurIPS, Springer LNCS. Each has its own style file.
4. **Anonymize for double-blind** — remove names, references to your own work in 3rd person.
5. **Write a cover letter** — 1 page, why this paper fits the venue.
6. **Submit** — pay any fees, upload supplementary.
7. **Wait for review** — 2-6 months.
8. **Respond to reviewers** — see `06_Paper_And_Publishing/04`.

**Watch out:** Predatory journals (see `06_Paper_And_Publishing/03`).

**Next:** Present it.

---

## Stage 12 — Presentation (Slides + Poster + Talk)

**The 3-line theory:**
A good talk = 1 idea + 1 story + 1 demo. Most researchers over-explain. Aim for 1 slide per minute, big fonts, simple figures.

**Slide structure (15-min conference talk):**

| Slide # | Title | Content |
|---|---|---|
| 1 | Title | Title, authors, logos |
| 2 | Motivation | 1 problem + 1 image |
| 3 | Research question | 1 sentence |
| 4 | Gap | "What no one has done" |
| 5 | Our idea | 1 figure |
| 6 | Method | 1 architecture diagram |
| 7 | Experiment 1 | Main result table |
| 8 | Experiment 2 | Ablation |
| 9 | Discussion | Strengths + limitations |
| 10 | Take-home | 1 sentence summary |
| 11 | Thank you | Code link, contact |

**Tips:**

- Font ≥ 24 pt
- 1 idea per slide
- Use the figure from the paper, but simplified
- Practice out loud 5+ times
- Anticipate 20 questions

**Poster:** A0 portrait. Title at top, 4 columns: Intro, Method, Results, Conclusion. See `06_Paper_And_Publishing/06`.

**Next:** Write your thesis.

---

## Stage 13 — Your Thesis (Putting It All Together)

**The 3-line theory:**
The thesis = the paper × 6 chapters + a defense. Chapter 3 (Methodology) = your paper's Method section, expanded. Chapter 4 (Results) = your paper's Results + ablations, expanded. The other chapters are framing.

**Chapter structure (target lengths):**

| Chapter | Pages | What |
|---|---|---|
| 1. Introduction | 10-15 | Why this matters, RQs, contribution |
| 2. Literature Review | 15-25 | The 30-100 papers, grouped, ending with the gap |
| 3. Methodology | 15-20 | Data, methods, setup, justified |
| 4. Results | 15-20 | Main results, ablations, analysis, figures, tables |
| 5. Discussion | 10-15 | What it means, limitations, future work |
| 6. Conclusion | 3-5 | Summary, contribution, impact |
| Bibliography | 5-10 | All references |
| Appendices | 5-15 | Extra figures, code, math |

**Defense:** 15-20 slides, 20-30 min talk, 30 min questions. Practice 5+ times. Know your limitations. Smile. See `07_My_Thesis/03_Thesis_Defense_Prep`.

**Next:** Defend and graduate. 🎓

---

## 🔁 The Loop Is Continuous

Even after publishing, research continues:
- Other people cite your work
- You write a follow-up
- You generalize to another domain
- You teach others what you learned

**That feedback loop is what makes you a researcher.**

---

## ✅ Done When (overall)

- [ ] You have a thesis topic
- [ ] You read 30+ papers
- [ ] You have a working pipeline
- [ ] You have a baseline AND a proposed method
- [ ] You have a main-results table
- [ ] You have an ablation table
- [ ] You have statistical tests
- [ ] Your code is on GitHub, reproducible
- [ ] You have a paper draft
- [ ] You submitted to arXiv
- [ ] You made slides + poster
- [ ] You wrote your thesis chapters
- [ ] You defended
- [ ] 🎓 You are MSc Abdur Rahman 🎓

---

**Open `CHECKLISTS.md` next for the tickable version of every step above.**
