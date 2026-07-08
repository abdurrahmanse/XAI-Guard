# 01 — How To Use This Repo

> **Welcome! This is your research foundation. Open this file first.**

---

## 🎯 What This Repo Is

A **complete, reusable knowledge base** for doing Data Science research — from "I have no topic" to "I have a published paper."

It is designed to be:

| Property | Meaning |
|---|---|
| **Simple** | Plain English. No jargon without explanation. |
| **Complete** | Covers every stage of the research workflow. |
| **Reusable** | Copy `00_Project_Template/` for any new project. |
| **Theory + Code** | Every topic has math, intuition, and copy-paste code. |
| **Beginner → Advanced** | Start at the top, work your way down. |

---

## 📖 How To Read It

There are **3 ways** to use this repo. Pick the one that fits your stage.

### Way 1: I'm new to research (beginner)

1. Open `00_START_HERE/02_What_Is_Research.md` (next file)
2. Read `RESEARCH_PROCESS.md` at the root — the end-to-end story
3. Walk the folders in order: `01_Research_Basics` → `02_Math_And_Stats` → ... → `07_My_Thesis`
4. Tick boxes in `CHECKLISTS.md` as you go

### Way 2: I have a topic and need to start a project

1. Read `RESEARCH_PROCESS.md` for the linear workflow
2. Copy `00_Project_Template/` to a new folder for your project
3. Open `CHECKLISTS.md` and start ticking off stages
4. Jump to whichever folder matches your current stage (e.g., `04_Data_Work` for preprocessing)

### Way 3: I just need a quick answer (advanced)

- Use `TEMPLATES/` for copy-paste starting points
- Open the folder for your current stage
- Each file is self-contained with theory + code

---

## 🗂️ Folder Map (at a glance)

| Folder | What It Covers |
|---|---|
| `00_START_HERE/` | You are here. Reading guide + roadmap. |
| `01_Research_Basics/` | How research works, reading papers, picking a topic, ethics |
| `02_Math_And_Stats/` | Linear algebra, probability, hypothesis testing, calculus, optimization |
| `03_Tools/` | Python, Git, LaTeX, IDEs, experiment tracking, environments, CLI |
| `04_Data_Work/` | Collection, cleaning, EDA, feature engineering, splits, imbalanced data, images, text |
| `05_Machine_Learning/` | Classical ML, deep learning, CV, NLP, time series, RL, transfer learning, evaluation, tuning, reproducibility |
| `06_Paper_And_Publishing/` | Writing papers, literature review, publishing, responding to reviewers, presentations |
| `07_My_Thesis/` | Proposal, drafts, defense, weekly logs, advisor notes |
| `TEMPLATES/` | Copy-paste templates (README, notebook, config, proposal, etc.) |
| `00_Project_Template/` | A complete, copy-paste skeleton for any new project |
| `RESEARCH_PROCESS.md` | The single end-to-end guide from idea to paper |
| `CHECKLISTS.md` | Master checklist — one list per research stage |

---

## 🔁 Reusable Project Template

Whenever you start a **new** research project:

```bash
# Copy the template folder to your new project location
cp -r 00_Project_Template/ ~/projects/my-new-research/

# Then rename, edit the README, and start working
```

This gives you a **ready-made structure** with `data/`, `src/`, `notebooks/`, `experiments/`, `results/`, `configs/`, `docs/`, `references/`, `reports/` — all the folders you need.

---

## ✅ Done When

- [ ] You know what this repo is
- [ ] You picked your reading way (1, 2, or 3 above)
- [ ] You opened the folder that matches your current stage
- [ ] You started ticking `CHECKLISTS.md`

Next file: **`02_What_Is_Research.md`**
