# 01 — How Research Works

> **Learn what research is, how to read papers, and how to pick a topic.**

---

## 📚 4 Things To Learn

| # | Topic | Time |
|---|---|---|
| 01 | How research works | 2 days |
| 02 | How to read papers | 3 days |
| 03 | How to pick a topic | 2 days |
| 04 | Research ethics | 2 days |

---

## 01. How Research Works

Research = **finding answers to questions** that no one has answered before.

**Simple process:**
1. Find a question
2. Read what others did
3. Try a new method
4. See if it works
5. Tell others what you found

---

## 02. How To Read Papers

**The 3-Pass Method:**

| Pass | Time | What To Do |
|---|---|---|
| Pass 1 | 10 min | Read title, abstract, conclusion |
| Pass 2 | 1 hour | Read full paper, skip hard parts |
| Pass 3 | 3 hours | Read carefully, understand everything |

**Where to find papers:**
- Google Scholar: scholar.google.com
- arXiv: arxiv.org
- Papers With Code: paperswithcode.com

---

## 03. How To Pick A Topic

**Good topic checklist:**
- [ ] You find it interesting
- [ ] It solves a real problem
- [ ] Data is available
- [ ] It's doable in your time
- [ ] Your advisor agrees

**Tip:** Look at recent papers. What questions are still open?

---

## 04. Research Ethics

**Always:**
- Be honest
- Give credit to others
- Protect people's data
- Don't make up results
- Share your code & data

---

## ✏️ Practice Exercises

### Exercise 1: Define Research (Easy)
**Time:** 30 minutes
**Task:** Write your own definition of "research" in 2-3 sentences.
**Why:** Helps you understand the concept in your own words.

**How to do it:**
1. Open a new file called `my_research_definition.md`
2. Answer these questions:
   - What is research to you?
   - How is it different from a school project?
   - Why does research matter?
3. Write 2-3 sentences for each
4. Compare with 2 classmates or friends

**Example answer:**
> "Research is solving a question that nobody has solved before. Unlike a school project, research adds new knowledge to the world. It matters because it helps us understand things better."

---

### Exercise 2: Find 3 Research Questions (Medium)
**Time:** 1 hour
**Task:** Find 3 research questions in Data Science.
**Why:** Practice identifying what makes a good research question.

**How to do it:**
1. Go to Google Scholar
2. Search: "machine learning" + "open problem"
3. Look at 5 recent papers
4. Read their "Conclusion" and "Future Work" sections
5. Write down 3 questions you find interesting

**Write in this format:**
```
Question 1: Can transformers detect fake news better than traditional ML?
Found in: Paper by Smith et al. (2024)
Why interesting: It's a real problem
```

---

### Exercise 3: Compare Research Types (Medium)
**Time:** 1 hour
**Task:** Find 1 example of each type of research.
**Why:** Understand different kinds of research.

**How to do it:**
Search Google Scholar for:
1. **Basic research** (e.g., "new neural network architecture")
2. **Applied research** (e.g., "ML for medical diagnosis")
3. **Experimental** (e.g., "A/B test results")
4. **Observational** (e.g., "social media analysis")

For each, write:
- Title
- Authors
- Year
- One-line summary
- Why it's this type

---

### Exercise 4: Write Your Research Goals (Easy)
**Time:** 30 minutes
**Task:** Write down why you want to do research.
**Why:** Clarify your motivation.

**How to do it:**
Answer these questions in writing:
1. Why am I doing this MSc?
2. What do I want to learn?
3. Where do I see myself in 3 years?
4. What kind of researcher do I want to be?

Save it. Read it again in 6 months.

---

## ✅ Done When

- [ ] You can explain what research is
- [ ] You read 5 papers using 3-pass method
- [ ] You have 3 topic ideas
- [ ] You know basic ethics rules
- [ ] You completed all 4 exercises

---

## 📘 Deep Dive: The Anatomy Of A Research Project

> A more advanced view. Read this once you've done the basics above.

### The "Research Diamond" — 4 Phases

Most research projects follow this 4-phase shape. Knowing it helps you know where you are.

```
            ┌──────────┐
            │ DISCOVER │   ← idea, lit review, gap-finding
            └────┬─────┘
                 ↓
            ┌──────────┐
            │  DESIGN  │   ← method, baselines, evaluation plan
            └────┬─────┘
                 ↓
            ┌──────────┐
            │ EXECUTE  │   ← run experiments, debug, iterate
            └────┬─────┘
                 ↓
            ┌──────────┐
            │  SHARE   │   ← paper, talk, code, dataset
            └──────────┘
```

**DISCOVER (10-20% of time):** Read, brainstorm, find a gap.
**DESIGN (10-15%):** Plan methods, baselines, metrics.
**EXECUTE (50-60%):** Run experiments, debug, iterate. This is where most of your time goes.
**SHARE (15-25%):** Write, present, publish.

### The 4 Types Of Contributions

In a Data Science paper, your contribution usually falls into one of these:

| Type | Example | Easiest? |
|---|---|---|
| **New method** | A new neural architecture | ❌ Hard |
| **New application** | Apply LLM to medical records | ✅ Medium |
| **New analysis** | Error analysis of GPT-4 on X task | ✅ Medium |
| **New dataset** | Release a labeled corpus | ⚠️ Hard (needs data) |
| **New evaluation** | A better metric for Y | ⚠️ Hard (needs buy-in) |
| **Stronger baseline** | A really good reproducible baseline | ✅ Easy and useful |
| **Survey / review** | A systematic review of 100 papers | ✅ Easy to start, hard to finish |

**For an MSc thesis, "new application" or "stronger baseline" is totally fine.** You don't need to invent a new architecture.

### The "Good Enough" Bar

| What "good" looks like for an MSc | What reviewers want for top venues |
|---|---|
| 1 clear research question | Multiple sub-questions, each answered |
| 1 dataset, 1-2 baselines | 3+ datasets, 5+ baselines, SOTA comparison |
| 1 metric reported properly | 5+ metrics, ablations, statistical tests |
| Reproducible code on GitHub | Reproducible code + Docker + configs |
| 1 paper draft | 2+ papers (workshop + main venue) |
| 1 presentation | Talk + poster + demo |

**Don't compare yourself to PhD students with 5 years.** Aim for "good enough" + "honest."

### The 5 Things That Will Go Wrong (and what to do)

| Problem | Solution |
|---|---|
| "My model doesn't beat the baseline" | Try 3 more baselines; check data leakage; use a different metric |
| "I don't have enough data" | Use transfer learning; augment; use public data |
| "It takes 10 hours to run" | Use a subset; use a smaller model; use Colab GPU |
| "I can't find related work" | Search Google Scholar "since 2023" + arXiv; ask your advisor |
| "I have no idea what to do" | Read 1 paper, do 1 experiment, write 1 sentence — repeat |

### The "Just Start" Rule

Most students wait until they have the perfect plan. **Don't.** Your plan will change. The fastest way to learn what to do is to start doing something — and then adjust.

The minimum viable first week:

1. Pick a topic
2. Find 1 public dataset
3. Run 1 baseline
4. Write 1 paragraph

That's it. Now you have a project. Everything else is iteration.

### Resources For Going Deeper

| Resource | Use |
|---|---|
| "How to Write a Good Scientific Paper" by Chris A. Mack | Writing |
| "Deep Learning" by Goodfellow, Bengio, Courville | Theory |
| "The Elements of Statistical Learning" (Hastie, Tibshirani, Friedman) | Classical ML |
| Andrew Ng's Machine Learning Yearning (free PDF) | ML strategy |
| Justin Solomon's "6.S898 Deep Learning" (MIT OCW) | Applied DL |

---

## ✅ Advanced "Done When"

- [ ] You can name the 4 phases of the research diamond
- [ ] You can name 3 types of research contributions
- [ ] You know the "good enough" bar for an MSc
- [ ] You can list 3 things that will go wrong and how to handle them
- [ ] You started your first baseline (even if ugly)
