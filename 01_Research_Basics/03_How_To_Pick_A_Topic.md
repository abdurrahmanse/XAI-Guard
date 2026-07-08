# 03 — How To Pick A Topic

> **Your MSc topic will define 1-2 years of your life. Choose wisely.**

---

## 5 Steps To Pick A Good Topic

### Step 1: Find Your Interest
Ask yourself:
- What data science topics excite you?
- What problems do you want to solve?
- What courses did you love?

### Step 2: Find Available Data
Without data, no research. Check:
- Kaggle datasets
- UCI Repository
- Your university (some have data)
- Government websites
- APIs

### Step 3: Find The Gap
- Read 20-30 recent papers in your area
- Look at "Future Work" sections
- What did they not do?

### Step 4: Talk To Professors
- Email 3-5 professors
- Ask if they have ideas
- Discuss your interests
- Find your thesis advisor

### Step 5: Write The Proposal
- Problem statement (1 page)
- Research questions (3-5)
- Method you plan to use
- Expected contribution

---

## Good Topic Examples

| Field | Example Topic |
|---|---|
| Healthcare | Predict diabetes from EHR data |
| NLP | Detect fake news with transformers |
| Computer Vision | Detect tumors in X-ray images |
| Finance | Predict stock prices with LSTM |
| Social Media | Analyze sentiment during elections |

---

## ❌ Bad Topics

- Too broad: "Study all of AI"
- Too narrow: "Predict one number"
- No data: "Predict aliens' behavior"
- Already solved: "Make MNIST classifier"

---

## ✏️ Practice Exercises

### Exercise 1: Brainstorm 10 Topics (Easy)
**Time:** 1 hour
**Task:** Write down 10 possible MSc topics.
**Why:** You need options before you can pick.

**How to do it:**
1. Open a new file: `topic_ideas.md`
2. Set a timer for 30 minutes
3. Don't stop. Write 10 ideas. They can be silly.
4. After 30 min, pick the top 3

**Format:**
```
Topic 1: Predict house prices
Topic 2: Detect fraud in credit cards
Topic 3: ...
```

---

### Exercise 2: Check Data Availability (Easy)
**Time:** 2 hours
**Task:** Find data for your top 3 topics.
**Why:** No data = no research.

**How to do it:**
For each of your top 3 topics:
1. Search Kaggle, UCI, Google Dataset Search
2. If found: save the link, note the size, format
3. If not found: search for "your topic" + "dataset" + "github"
4. If still not: try government sites, APIs

**Write down:**
- Topic name
- Data found? (Yes/No)
- Source
- Size (rows × columns)
- License (can you use it?)

---

### Exercise 3: Write 1 Research Question (Medium)
**Time:** 1 hour
**Task:** Write 1 strong research question for your favorite topic.
**Why:** A good question = good research.

**How to do it:**
Use this template:
```
Can [METHOD] improve [METRIC] for [PROBLEM] compared to [BASELINE] on [DATASET]?
```

**Examples:**
- "Can transformers improve accuracy for fake news detection compared to logistic regression on the FakeNewsNet dataset?"
- "Can LSTM predict stock prices better than ARIMA on Tesla stock data?"

---

### Exercise 4: Find The Gap (Medium)
**Time:** 3 hours
**Task:** Read 10 recent papers in your area. Find the gap.
**Why:** Your thesis should fill a gap. No gap = no thesis.

**How to do it:**
1. Google Scholar: "your topic" (last 2 years)
2. Pick 10 papers
3. For each, write:
   - Method used
   - Dataset used
   - Main result
   - Limitation / future work
4. Look at the 10 limitations
5. Find what NONE of them did

**Write the gap as 1 sentence:**
"The gap is: nobody has used [YOUR METHOD] on [YOUR DATA] to solve [YOUR PROBLEM]."

---

### Exercise 5: Email A Professor (Hard but important)
**Time:** 1 hour
**Task:** Email 3 professors about your topic.
**Why:** You need an advisor. Start the conversation.

**How to do it:**
1. Find 3 professors in your area
2. Read 1 of their recent papers
3. Write a short email (5-7 sentences):

**Template:**
```
Subject: MSc Thesis Inquiry - [Your Topic]

Dear Professor [Name],

I'm an MSc Data Science student at [University]. I'm interested in
[topic] and read your paper "[paper title]" with great interest.

I would like to explore [specific question] in my thesis.
Could we meet to discuss this?

I have attached my CV and a 1-page topic idea.

Best regards,
[Your Name]
```

4. Send to 3 professors
5. Wait for replies (1-2 weeks)

---

## ✅ Done When

- [ ] You have 3 topic ideas
- [ ] You have data for your favorite
- [ ] You wrote a 1-page problem statement
- [ ] A professor agreed to supervise
- [ ] You completed all 5 exercises

---

## 🧠 The 4-Criteria Filter

A good topic must pass ALL 4 filters. Test yours:

| # | Criterion | Test |
|---|---|---|
| 1 | **Interesting to you** | Will you still care in 6 months? |
| 2 | **Solves a real problem** | Does anyone care about the result? |
| 3 | **Data is available** | Can you get the data legally + in time? |
| 4 | **Doable in time** | Can you finish in 3-6 months? |

If any one fails, drop the topic and pick another.

## 🔍 The "Topic Sources" List (use these to find ideas)

| Source | How To Use It |
|---|---|
| **Papers With Code SOTA** | paperswithcode.com/sota → see what's being solved |
| **Kaggle competitions** | kaggle.com/competitions → trending problems |
| **arXiv recent** | arxiv.org/list/cs.LG/2025 → last week's papers |
| **AI conference deadlines** | aideadlin.es → see what areas are active |
| **Your university research groups** | Read the lab pages, find an open problem |
| **Industry pain points** | "ML for [X]" — find a X that's unsolved |
| **Public datasets (UCI, Kaggle)** | A new dataset = a research opportunity |
| **Your course projects** | Many theses start as good course projects |
| **Failed papers** | A paper that didn't work → investigate why |
| **Negative results** | "We tried X, it didn't work" is publishable |

## ✍️ The "Research Question" Template

Use this exact format. If you can't fill it, your topic is too vague.

```
Can [METHOD] improve [METRIC] for [PROBLEM] 
    compared to [BASELINE] on [DATASET]?
```

**Examples:**

| Method | Problem | Dataset | Baseline | Metric |
|---|---|---|---|---|
| Domain-adapted BERT | Fake news detection | FakeNewsNet | Standard BERT | F1 |
| LSTM | Stock prediction | Tesla 5-yr | ARIMA | RMSE |
| 3D CNN | Tumor segmentation | BraTS 2024 | 2D U-Net | Dice |
| Transformer | Code summarization | Python corpus | LSTM | BLEU |

If you can write this sentence, you have a topic.

## 🌳 The "Topic Tree" (zoom in or out)

```
Healthcare
├── Medical Imaging
│   ├── X-ray → ?
│   ├── MRI → ?
│   └── CT → ?
├── EHR data
│   ├── Prediction → ?
│   └── Risk scoring → ?
└── Genomics
    └── ...
```

Pick a branch. Then a leaf. Then a sub-leaf. That sub-leaf is your topic.

## ⚖️ Comparing 3 Topic Candidates

Use this matrix:

| Criterion | Topic A | Topic B | Topic C |
|---|---|---|---|
| Novelty (1-5) | 4 | 3 | 5 |
| Data availability (1-5) | 5 | 4 | 2 |
| Advisor interest (1-5) | 5 | 3 | 4 |
| Your interest (1-5) | 4 | 5 | 3 |
| Doability (1-5) | 4 | 4 | 2 |
| **Total** | **22** | **19** | **16** |

**Pick the highest total.** If 2 are tied, pick the one with the highest "Your interest."

## 📅 The "1-Week Topic Test"

| Day | Task |
|---|---|
| Mon | Pick 3 candidate topics |
| Tue | Search data for each |
| Wed | Read 2 papers per topic (6 total) |
| Thu | Email 2 professors per topic |
| Fri | Pick the winner. Write a 1-page problem statement. |
| Sat-Sun | Rest. Then start reading. |

If after 1 week you don't have a winner, your filters are too strict. Loosen them.

## 🤝 Picking An Advisor (quick guide)

| What to look for | Red flags |
|---|---|
| Works in your topic area | Hasn't published in 3 years |
| Has supervised MSc students before | Takes 2 months to reply to emails |
| Has funding for your topic | Forces you to work on their pet project |
| Respects your time | Wants daily 9am meetings |
| Replies within 1 week | "Just figure it out" answers |

**Email 5 professors, expect 2 to reply, meet 2, pick 1.**

## ✅ Advanced "Done When"

- [ ] Your topic passes the 4-criteria filter
- [ ] You can write the "Can [METHOD] improve [METRIC]..." sentence
- [ ] You used the topic tree to zoom in
- [ ] You scored 3 candidates with the matrix
- [ ] You did the 1-week topic test
- [ ] An advisor said yes
