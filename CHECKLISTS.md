# CHECKLISTS.md — Master Checklists For Every Stage

> **Print this file. Tick boxes as you go. Re-print when full.**

---

## Stage 0 — Mindset

- [ ] I read `00_START_HERE/02_What_Is_Research.md`
- [ ] I can explain the difference between a school project and research
- [ ] I know the 3 types of research (basic, applied, experimental)
- [ ] I can draw the research loop from memory
- [ ] I picked a domain I care about

---

## Stage 1 — Idea Generation

- [ ] I brainstormed 10 topic ideas
- [ ] I picked my top 3
- [ ] I found data for each
- [ ] I checked feasibility (time, data, advisor)
- [ ] I wrote 1 strong research question (using the template)
- [ ] I read `01_Research_Basics/05_Idea_Generation_Methods.md`

---

## Stage 2 — Literature Review

- [ ] I defined 3-5 search keywords
- [ ] I searched Google Scholar, arXiv, IEEE Xplore
- [ ] I read 30+ papers using the 3-pass method
- [ ] I filled in a comparison spreadsheet
- [ ] I grouped papers by theme
- [ ] I found **the gap** (1 sentence)
- [ ] I wrote 10+ pages of lit review draft
- [ ] I built a comparison table of methods

---

## Stage 3 — Project Setup

- [ ] I copied `00_Project_Template/` to a new folder
- [ ] I created a virtual environment
- [ ] I wrote `requirements.txt`
- [ ] I set up Git + pushed to GitHub
- [ ] I installed LaTeX (or use Overleaf)
- [ ] I installed Zotero
- [ ] I set up an experiment tracker (MLflow or W&B)
- [ ] I set up an IDE (VSCode or Jupyter)
- [ ] I filled in the project README

---

## Stage 4 — Data Work

- [ ] I found/collected the dataset
- [ ] I checked the license (can I use it?)
- [ ] I checked shape, dtypes, missing values
- [ ] I removed duplicates
- [ ] I handled missing values
- [ ] I handled outliers
- [ ] I fixed data types
- [ ] I did EDA (5+ charts, 3+ insights)
- [ ] I engineered features (3+ new)
- [ ] I encoded categoricals
- [ ] I scaled numerics
- [ ] I split train/val/test (no leakage)
- [ ] I saved cleaned data to `data/processed/`
- [ ] I wrote a data card (see `TEMPLATES/data_card_template.md`)

---

## Stage 5 — Baseline

- [ ] I built a "most frequent" baseline
- [ ] I built a logistic regression baseline
- [ ] I built a tree-based baseline (RF or XGBoost)
- [ ] I used cross-validation (5-fold)
- [ ] I reported mean ± std
- [ ] I saved baseline results to `results/tables/baselines.csv`

---

## Stage 6 — Method (Proposed)

- [ ] I can describe my method in 3 sentences to a non-expert
- [ ] I can describe it in 30 seconds (the "elevator pitch")
- [ ] I implemented it cleanly in `src/models/`
- [ ] I have a config file in `configs/`
- [ ] I have a training script in `experiments/`
- [ ] I logged the run in MLflow / W&B
- [ ] I tested on a small subset first (sanity check)

---

## Stage 7 — Experiments

- [ ] I ran 5+ seeds for the main result
- [ ] I ran all baselines with the same seeds
- [ ] I ran ablations (one design choice off at a time)
- [ ] I tracked every run in MLflow
- [ ] I saved all figures to `results/figures/`
- [ ] I saved all tables to `results/tables/`
- [ ] I wrote a short summary of what I found

---

## Stage 8 — Evaluation

- [ ] I picked the right metric (F1, MAE, etc.) for my task
- [ ] I reported a confusion matrix (classification)
- [ ] I reported predicted-vs-actual (regression)
- [ ] I reported a main results table
- [ ] I reported an ablation table
- [ ] I ran a statistical test (t-test) to compare methods
- [ ] I computed effect size (Cohen's d)
- [ ] I made a learning-curve plot
- [ ] I did an error analysis (looked at the wrong predictions)

---

## Stage 9 — Documentation & Reproducibility

- [ ] I set a global seed (and used it everywhere)
- [ ] I have a clean `README.md` (what, install, run)
- [ ] I have `requirements.txt` (or `environment.yml`)
- [ ] I have a license (MIT, Apache 2.0, etc.)
- [ ] I have a data card
- [ ] I have a model card
- [ ] I pushed all code to GitHub
- [ ] I tagged a release
- [ ] A friend can run my code and get similar numbers

---

## Stage 10 — Writing The Paper

- [ ] I picked a target venue (conference or journal)
- [ ] I downloaded the right template
- [ ] I wrote the abstract (5 sentences)
- [ ] I wrote the introduction (problem + gap + contribution)
- [ ] I wrote related work (how my work fits)
- [ ] I wrote methods (with enough detail to reproduce)
- [ ] I wrote experiments (setup + results + ablations)
- [ ] I wrote discussion (limitations + future work)
- [ ] I wrote conclusion
- [ ] I cited all 30+ papers
- [ ] I proofread 3 times
- [ ] I had 2 friends review it
- [ ] I checked the page limit
- [ ] I checked the template rules (anonymization, etc.)

---

## Stage 11 — Publishing

- [ ] I uploaded to arXiv
- [ ] I picked 3 target venues
- [ ] I anonymized for double-blind
- [ ] I wrote a cover letter
- [ ] I submitted to venue #1
- [ ] I waited for reviews
- [ ] I responded to reviewers (see `06_Paper_And_Publishing/04`)
- [ ] I made revisions
- [ ] I celebrated acceptance 🎉

---

## Stage 12 — Presentation

- [ ] I made 15-20 slides
- [ ] I used big fonts (≥ 24 pt)
- [ ] I included 1 figure per slide
- [ ] I practiced out loud 5+ times
- [ ] I anticipated 20 questions
- [ ] I knew my limitations
- [ ] I made a poster (A0 portrait)
- [ ] I gave the talk
- [ ] I shared my slides on GitHub

---

## Stage 13 — Thesis

- [ ] I wrote Chapter 1 (Introduction)
- [ ] I wrote Chapter 2 (Literature Review)
- [ ] I wrote Chapter 3 (Methodology)
- [ ] I wrote Chapter 4 (Results)
- [ ] I wrote Chapter 5 (Discussion)
- [ ] I wrote Chapter 6 (Conclusion)
- [ ] I compiled references
- [ ] I added appendices
- [ ] I had 3 proofreaders
- [ ] My advisor approved
- [ ] I made defense slides
- [ ] I practiced the defense
- [ ] I defended
- [ ] I submitted final PDF
- [ ] I graduated 🎓

---

## 🏁 Final State (the "you're done" checklist)

- [ ] GitHub: public repo with code + README
- [ ] arXiv: paper is up
- [ ] Conference/journal: submitted (or accepted)
- [ ] Thesis: defended and submitted
- [ ] You have a Google Scholar / ORCID profile
- [ ] You can present your work in 5 minutes
- [ ] You can list 3 things you learned
- [ ] You can name 3 things that didn't work
- [ ] You have a plan for the next project
- [ ] **You are a researcher.** 🧑‍🔬

---

**When all boxes are ticked: congratulations, MSc! 🎓**
