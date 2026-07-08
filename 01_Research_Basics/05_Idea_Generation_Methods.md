# 05 — Idea Generation Methods

> **Stuck on "what should I work on?" Here are 10 methods that actually work.**

---

## 🧠 Method 1: The "Reading-Into-Ideas" Method

**Time:** 2 weeks
**Steps:**
1. Read 20 papers in your broad area
2. For each paper, write in your notes:
   - "What was good?"
   - "What was missing?"
   - "What would I do differently?"
3. Patterns emerge. The "would I do differently" is your idea.

**Example output:**
> "10 papers used BERT-base. None used domain-adapted BERT for X. **Idea: domain-adapt BERT on X.**"

---

## 🧠 Method 2: The "Combine Two Things" Method

**Time:** 1 day
**Steps:**
1. Make a list of 5 popular methods (e.g., BERT, ResNet, XGBoost, LSTM, Transformer)
2. Make a list of 5 popular domains (e.g., healthcare, finance, education, climate, agriculture)
3. Make a list of 5 popular tasks (e.g., classification, generation, detection, prediction, ranking)
4. Pick any combination **that no one has combined before**
5. Search Google Scholar to confirm the gap

**Example:**
- Methods: {BERT, LSTM, XGBoost, ResNet, Transformer}
- Domains: {legal, medical, education, finance, art}
- Pick: "Transformer + legal" → check if anyone has done **legal contract classification with transformers**. If not, that's your topic.

---

## 🧠 Method 3: The "Failure Analysis" Method

**Time:** 3 days
**Steps:**
1. Find 5 papers that got **state-of-the-art** on a benchmark
2. For each, look for:
   - Datasets they tested on (any missing?)
   - Languages they tested in (only English?)
   - Demographic groups they tested on (only adults?)
   - Conditions they tested in (only clean data?)
3. The **untested** condition is your idea.

**Examples:**
- "BERT was tested on English news, not on African languages" → idea
- "ResNet was tested on clean X-rays, not on low-dose X-rays" → idea
- "GPT-4 was tested on short prompts, not on long prompts" → idea

---

## 🧠 Method 4: The "Practitioner Pain Points" Method

**Time:** 1 week
**Steps:**
1. Find 5 people who **do the job** you're interested in (doctors, teachers, lawyers)
2. Ask them: "What takes too much of your time? What do you wish you could automate?"
3. Pick a pain point that is **measurable** and has **data**

**Example outputs from real interviews:**
- Doctors: "Writing patient summaries takes 30 min per patient"
- Teachers: "Grading essays takes hours"
- Lawyers: "Searching through case law takes days"
- Bankers: "Reading 10-K filings takes a week"

Each of these is a thesis topic.

---

## 🧠 Method 5: The "Datasets Are Ideas" Method

**Time:** 2 days
**Steps:**
1. Browse **Papers With Code Datasets** (paperswithcode.com/datasets)
2. Browse **Kaggle Datasets** (kaggle.com/datasets)
3. Browse **Hugging Face Datasets** (huggingface.co/datasets)
4. Find a **new** dataset (released in the last 6 months)
5. The first paper to use that dataset is your idea

**Why this works:** Datasets are hard to make. If someone released one, they want people to use it. You being "the first to try X on this dataset" is a real contribution.

---

## 🧠 Method 6: The "Workshop Topics" Method

**Time:** 1 day
**Steps:**
1. Look at recent workshop CFPs (Calls for Papers) for top conferences
2. Workshops focus on **emerging** topics where they want more research
3. Pick a workshop topic that interests you
4. That topic is your thesis

**Where to look:**
- NeurIPS workshops: neurips.cc → workshops
- ICML workshops: icml.cc → workshops
- ACL workshops: aclweb.org → workshops
- ICLR workshops: iclr.cc → workshops

---

## 🧠 Method 7: The "Old Idea, New Tool" Method

**Time:** 1 week
**Steps:**
1. Pick an old, hard problem (e.g., "machine translation" — 70 years old)
2. Pick a new tool (e.g., "LLM" — released last year)
3. Apply the new tool to the old problem
4. If it works, that's a paper

**Examples:**
- Old: "text classification" + New: "LLM" → LLM zero-shot classification
- Old: "time series forecasting" + New: "transformer" → Transformer for forecasting
- Old: "image segmentation" + New: "diffusion model" → Diffusion for segmentation

---

## 🧠 Method 8: The "Reproduce and Improve" Method

**Time:** 2-3 weeks
**Steps:**
1. Find a strong paper with **public code**
2. Try to reproduce it (this alone is a contribution)
3. Find a small weakness in their method
4. Improve that weakness
5. Write a paper: "We reproduce [X] and improve it by [Y]"

**Why this works:**
- "Reproducibility studies" are increasingly respected
- You don't need a brand-new idea
- You learn the field deeply
- The improvement can be small but real

---

## 🧠 Method 9: The "Negative Result" Method

**Time:** 1 week
**Steps:**
1. Find a method that's been claimed to work well
2. Try it on a different domain or dataset
3. If it doesn't work — that's a **negative result**, which is publishable
4. Title: "[Method X] does not generalize to [Domain Y]: an empirical study"

**Why this works:**
- Negative results prevent others from wasting time
- Journals like "Journal of Negative Results" exist
- They're easier to do (you're not trying to beat SOTA)
- They show scientific honesty

---

## 🧠 Method 10: The "Survey" Method

**Time:** 4-6 weeks
**Steps:**
1. Pick a topic (e.g., "deep learning for medical imaging")
2. Read 50-100 papers systematically
3. Group them by method, dataset, or task
4. Build comparison tables
5. Identify open problems
6. Write a 20-page survey

**Why this works:**
- You become the **expert** in that sub-area
- Surveys are highly cited
- You can then say "after my survey, I noticed gap X" and propose a method

---

## 📋 The "Generate 10 Ideas" Exercise

| # | Idea | Method Used | Novel? | Data? | Doable? | Score (1-5 each) |
|---|---|---|---|---|---|---|
| 1 | | | | | | |
| 2 | | | | | | |
| ... | | | | | | |
| 10 | | | | | | |

After 30 minutes, **score** each on 3 criteria (1-5). The top 3 are your candidates.

## 📋 "Test the Gap" Exercise

For your top 3 ideas:
1. Search Google Scholar: "exact title" → 0 results? Good.
2. Search for the **closest** existing work
3. Write the gap: "No one has [METHOD] on [DATA] for [PROBLEM]"
4. If you can't write that sentence, the idea is not specific enough.

## ⚠️ When You're Still Stuck

- **Take a walk.** Seriously. Many "Aha!" moments come during a walk.
- **Talk to people.** Friends, family, professors. Explain what you do, and they often ask the question that unlocks the idea.
- **Sleep on it.** Literally. Your brain solves problems during sleep.
- **Switch topics for a day.** If you're stuck, work on something else.
- **Read 1 more paper.** Often the right paper is one you haven't read.

## ✅ Done When

- [ ] You tried 3+ methods above
- [ ] You have 10 ideas written down
- [ ] You scored each on 3 criteria
- [ ] You have 3 candidates
- [ ] You tested the gap (Google Scholar returns 0)
- [ ] You can write the "no one has..." sentence for your top 3
