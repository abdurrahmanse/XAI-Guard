# 02 — How To Read Papers

> **Reading papers is the #1 skill of a researcher.**

---

## The 3-Pass Method

### Pass 1: Skim (10 minutes)

1. Read the **title**
2. Read the **abstract**
3. Read the **section headers**
4. Read the **conclusion**
5. Look at the **figures**

👉 Goal: Should I read this paper more?

### Pass 2: Understand (1 hour)

1. Read the full paper
2. Skip the hard math
3. Understand the main idea
4. Highlight key points

👉 Goal: Can I explain the paper to a friend?

### Pass 3: Deep dive (3+ hours)

1. Read every word
2. Re-create the math
3. Question the methods
4. Find limitations

👉 Goal: Can I find weaknesses?

---

## Where To Find Papers

| Site | Link | Best For |
|---|---|---|
| Google Scholar | scholar.google.com | General |
| arXiv | arxiv.org | Latest research |
| Papers With Code | paperswithcode.com | ML with code |
| Semantic Scholar | semanticscholar.org | AI-powered search |

---

## Track Your Reading

Create a spreadsheet:

| Paper | Year | Method | Result | Limitation | Citation |
|---|---|---|---|---|---|
| Paper 1 | 2024 | X | Y | Z | ... |
| Paper 2 | 2023 | A | B | C | ... |

---

## ✏️ Practice Exercises

### Exercise 1: Read Your First Paper (Easy)
**Time:** 1-2 hours
**Task:** Read 1 paper using the 3-pass method.
**Why:** This is the most important skill for research.

**How to do it:**
1. Go to arxiv.org
2. Pick any recent ML paper
3. **Pass 1 (10 min):** Read title, abstract, conclusion only
4. **Pass 2 (1 hr):** Read the full paper
5. **Pass 3 (optional):** Re-read carefully

**Write down:**
- What is the paper about? (2 sentences)
- What method did they use?
- What was the main result?
- What is one weakness?

Save in: `my_first_paper_summary.md`

---

### Exercise 2: Read 5 Papers in One Week (Medium)
**Time:** 1 week
**Task:** Read 5 papers in 7 days.
**Why:** Build reading habit. This is what you'll do during your whole MSc.

**How to do it:**
- **Day 1:** Paper 1 (use 3-pass method)
- **Day 2:** Paper 2
- **Day 3:** Paper 3
- **Day 4:** Paper 4
- **Day 5:** Paper 5
- **Day 6-7:** Review your notes

**Tip:** Pick papers from the same topic. It's easier.

---

### Exercise 3: Build Your Reading Spreadsheet (Easy)
**Time:** 1 hour
**Task:** Create a spreadsheet of papers you read.
**Why:** Track what you've learned. You'll reference this for your thesis.

**How to do it:**
1. Open Google Sheets or Excel
2. Add columns: Title | Year | Authors | Method | Result | Limitation | My Notes | Citation
3. Add 5 papers
4. Use it for every paper you read

**Template:**
| Title | Year | Method | Result | Limitation | Citation |
|---|---|---|---|---|---|
| Attention is all you need | 2017 | Transformer | Better than RNN | Needs lots of data | Vaswani et al. |

---

### Exercise 4: Summarize 1 Paper Per Day (Hard but powerful)
**Time:** 30 min/day for 30 days
**Task:** Write a 200-word summary of 1 paper each day.
**Why:** By the end, you'll have read 30 papers. That's a strong start for your lit review.

**How to do it:**
- Set a daily alarm (same time every day)
- Pick 1 paper
- Read it (Pass 1 + Pass 2)
- Write 200 words: What is it? Why does it matter? How did they do it? What did they find?
- Save as: `paper_day_01.md`, `paper_day_02.md`, etc.

---

### Exercise 5: Find a "Survey Paper" (Easy)
**Time:** 30 minutes
**Task:** Find 1 survey paper in your interest area.
**Why:** Survey papers summarize 50-200 papers. Great for your lit review.

**How to do it:**
1. Google: "survey" + "machine learning" + "your topic"
2. Find a recent one (last 2 years)
3. Add it to your reading list
4. Read the abstract + intro

**Example searches:**
- "survey on deep learning for medical imaging"
- "systematic review on NLP applications"
- "survey on time series forecasting"

---

## ✅ Done When

- [ ] You read 5 papers using 3-pass method
- [ ] You set up Google Scholar alerts
- [ ] You have a reading spreadsheet
- [ ] You installed Zotero
- [ ] You completed all 5 exercises

---

## 📝 Note-Taking Template (copy this for every paper)

Save this as `paper_notes/<year>_<author>_<keyword>.md`:

```markdown
# [Title]

**Authors:** ...
**Venue:** NeurIPS 2023
**Link:** https://arxiv.org/abs/...
**Date read:** 2026-07-08

## 1-Pass Summary (10 min)
- **Problem:** ...
- **Method:** ...
- **Result:** ...
- **My take:** ...

## 2-Pass Notes (1 hour)
- **Key idea:** ...
- **Why it matters:** ...
- **How it works (in 3 sentences):** ...
- **Datasets used:** ...
- **Baselines compared:** ...
- **Main metric reported:** ...
- **Limitations I see:** ...

## 3-Pass Notes (3 hours)
- **Assumptions:** ...
- **Math I had to re-derive:** ...
- **What would break this:** ...
- **Could I reproduce this in 1 week?:** ...
- **How does it connect to my work?:** ...

## Quotes (use exact wording for citations)
> "..." (p. 3)

## Questions for my advisor / myself
1. ...
2. ...
```

## 🗂️ Folder Layout For Your Reading

```
literature/
├── papers/             ← PDFs (Zotero manages this)
├── notes/              ← your .md notes (one per paper)
├── summary.md          ← 1-line summary of every paper
├── comparison_table.md ← methods × datasets × metrics
└── gap.md              ← the gap you found (1 sentence)
```

## 📊 How To Build A Comparison Table

After 10+ papers, build a table like this (saved as `literature/comparison_table.md`):

| Paper | Year | Method | Backbone | Dataset | Metric | Reported Score | Limitations |
|---|---|---|---|---|---|---|---|
| Smith | 2023 | BERT-base | BERT | FakeNewsNet | F1 | 0.85 | no domain adapt |
| Lee | 2024 | RoBERTa + data aug | RoBERTa | FakeNewsNet | F1 | 0.87 | small aug set |
| Park | 2024 | LLM zero-shot | GPT-3.5 | FakeNewsNet | F1 | 0.83 | closed model |
| **You (planned)** | 2026 | ? | ? | FakeNewsNet | F1 | ? | ? |

**The last row is your thesis.** What number do you need to beat to make a contribution?

## 🔔 Set Up Alerts (do this once)

| Alert | How |
|---|---|
| Google Scholar | scholar.google.com → create alert for "your topic" |
| arXiv | arxiv.org → set up email alerts in `cs.LG`, `cs.CL`, `cs.CV` |
| Semantic Scholar | semanticscholar.org → follow authors |
| Twitter / X | follow the top 10 authors in your field |
| Connected Papers | connectedpapers.com → find related work |
| Litmaps | litmaps.com → visualize a paper's neighborhood |

## 🧠 How To Read 100 Papers In A Year

| Time budget | Target |
|---|---|
| 1 paper / week (2-3 hrs) | Conservative — 50 / year |
| 1 paper / 2 days | Strong — 100 / year |
| 1 paper / day (lite) | Hero mode — 200+ / year |

**Realistic target for MSc Year 1:** 50 papers. You'll re-read ~10 of them in Year 2.

## 🗣️ Paper-Reading Groups

Find 2-3 friends. Each week:
1. One person presents 1 paper (10 min)
2. Others ask questions (10 min)
3. Everyone takes notes

**This works.** A paper you discuss is a paper you remember.

## ✅ Advanced "Done When"

- [ ] You have a paper-notes template
- [ ] You have a `literature/` folder with notes
- [ ] You built a comparison table of 10+ papers
- [ ] You set up Google Scholar alerts
- [ ] You read 50 papers in your first year
