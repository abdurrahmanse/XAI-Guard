# 04 — Research Ethics

> **Be a good researcher. Follow the rules.**

---

## The 5 Rules Of Research Ethics

### 1. Be Honest
- Don't make up results
- Don't fake data
- If it failed, say it failed

### 2. Give Credit
- Cite everyone you used
- Don't copy others' work
- Acknowledge all contributors

### 3. Protect People
- Get consent for human data
- Anonymize personal info
- Follow GDPR (if in EU)

### 4. Share Your Work
- Make your code public
- Share your data (if possible)
- Allow others to reproduce

### 5. Be Fair
- Review others' work fairly
- Don't discriminate
- Disclose conflicts of interest

---

## Plagiarism = NEVER

| Type | What It Is | Example |
|---|---|---|
| Direct | Copy-paste | Copy a paragraph from Wikipedia |
| Self | Reuse your own | Submit same paper twice |
| Mosaic | Mix sources | Combine sentences from many papers |

**Always:**
- Use citations
- Use quotation marks for quotes
- Paraphrase in your own words
- Use plagiarism checker (Turnitin, Quetext)

---

## AI Tools (Be Careful!)

Using ChatGPT is okay for:
- ✅ Brainstorming
- ✅ Explaining concepts
- ✅ Editing grammar

But NOT for:
- ❌ Writing your paper
- ❌ Generating fake citations
- ❌ Doing your analysis

**Always disclose AI use in your methods section.**

---

## ✏️ Practice Exercises

### Exercise 1: Find Ethics Examples (Easy)
**Time:** 1 hour
**Task:** Find 3 real-world examples of research ethics violations.
**Why:** Learn what NOT to do.

**How to do it:**
1. Google: "famous research ethics violations"
2. Read 3 cases (suggestions below)
3. Write a summary for each

**Famous cases to look up:**
- HeLa cells (Henrietta Lacks) - consent issue
- Theranos - fake data
- Facebook emotional contagion study - consent
- Stanford prison experiment - harm to participants

**Format:**
```
Case: [Name]
What happened: [2 sentences]
What rule was broken: [rule number]
What we can learn: [1-2 sentences]
```

---

### Exercise 2: Make A Citation List (Easy)
**Time:** 1 hour
**Task:** Cite 5 sources properly.
**Why:** You MUST know how to cite. No exceptions.

**How to do it:**
Find 5 sources (papers, websites, books) and cite them in 3 styles:

**APA Style Example:**
```
Smith, J. (2024). Machine learning for healthcare. 
Nature Medicine, 12(3), 45-67.
```

**IEEE Style Example:**
```
[1] J. Smith, "Machine learning for healthcare," 
Nature Medicine, vol. 12, no. 3, pp. 45-67, 2024.
```

**MLA Style Example:**
```
Smith, John. "Machine Learning for Healthcare." 
Nature Medicine, vol. 12, no. 3, 2024, pp. 45-67.
```

**Tip:** Use Zotero to auto-generate citations.

---

### Exercise 3: Set Up A Plagiarism Checker (Easy)
**Time:** 30 minutes
**Task:** Test 1 of your old essays in a plagiarism checker.
**Why:** Catch issues before your professor does.

**How to do it:**
1. Go to quetext.com or smallseotools.com/plagiarism-checker
2. Copy 1 paragraph from your old essay
3. Paste it in
4. See the result
5. Fix any issues

**Note:** Your university probably uses Turnitin. Get familiar with it.

---

### Exercise 4: Write A Consent Form (Medium)
**Time:** 1-2 hours
**Task:** Write a sample consent form for a survey.
**Why:** You may need this for your research.

**How to do it:**
Pretend you are doing a survey about "Data Science student stress". Write:

1. **Study title**
2. **What is this study about?** (2-3 sentences)
3. **Why am I being asked to participate?** (1 sentence)
4. **What will I do?** (steps, time needed)
5. **Risks** (any risks?)
6. **Benefits** (any benefits?)
7. **Privacy** (how data is protected)
8. **Right to withdraw** (you can stop anytime)
9. **Contact info** (who to ask questions)
10. **Signature line**

Save it. You can adapt it later.

---

### Exercise 5: Decide What's Ethical (Medium)
**Time:** 1 hour
**Task:** Read 5 scenarios. Decide if they are ethical.
**Why:** Ethics is about judgment, not rules.

**How to do it:**
For each scenario, write: Ethical? Yes/No. Why?

**Scenarios:**
1. You used a public dataset and forgot to cite the original paper.
2. Your model failed, but you only report the successful experiments.
3. You share your code but the data is private (you explain why).
4. A friend wrote code for you. You don't list them as co-author.
5. You use ChatGPT to write 1 paragraph and don't mention it.

**Format:**
```
Scenario 1: [description]
Ethical? No
Why: Must cite data sources. Plagiarism rule.
```

---

## ✅ Done When

- [ ] You know the 5 rules
- [ ] You have a citation tool (Zotero)
- [ ] You understand plagiarism types
- [ ] You know your university's ethics policy
- [ ] You completed all 5 exercises

---

## 🏛️ Deeper Ethics For Data Science Research

### 1. Data Ethics

| Principle | What It Means | Example |
|---|---|---|
| Consent | People agreed to share their data | Survey respondents signed a form |
| Anonymity | No way to identify a person from your data | Strip names, IDs, exact dates |
| Privacy | Sensitive info is protected | Encrypt medical records at rest |
| License | You have the right to use the data | Check "Terms of Use" before scraping |
| Fairness | Your model doesn't discriminate | Check error rates across subgroups |

### 2. Algorithmic Bias

**The 3 types of bias to watch for:**

| Bias | What It Is | Example |
|---|---|---|
| **Historical bias** | World is biased; data reflects that | Hiring data from a sexist era |
| **Sampling bias** | Your data isn't representative | All images taken in daylight |
| **Algorithmic bias** | The model amplifies the bias | Loan model denies minorities more often |

**How to detect:** Compute metrics per subgroup (gender, race, age). If one group's accuracy is much lower → bias.

```python
# Fairness check
for subgroup in df["gender"].unique():
    mask = df["gender"] == subgroup
    score = f1_score(y[mask], y_pred[mask], average="macro")
    print(f"{subgroup}: F1 = {score:.3f}")
```

### 3. Dual Submission

**Never submit the same paper to 2 venues at once.** It wastes reviewers' time and can get you banned.

**Allowed:**
- Workshop paper → later expanded to a conference paper (cite the workshop)
- arXiv preprint → submit to conference (cite the arXiv)
- Conference paper → expanded to a journal version (with new content)

**Not allowed:**
- Same paper, two venues, same time
- Trivial extension (just adding a paragraph)

### 4. Authorship (Who is an author?)

| Should be an author | Should NOT be an author |
|---|---|
| Wrote significant text | Just gave feedback |
| Did the experiments | Just provided data |
| Designed the method | Just paid for it |
| Wrote the code | Just edited grammar |
| Analyzed the results | A friend who "helped" |

**CRediT taxonomy** is the standard:

- Conceptualization, Methodology, Software, Validation, Formal analysis, Investigation, Data curation, Writing – original draft, Writing – review & editing, Visualization, Supervision, Project administration, Funding acquisition

### 5. Conflicts Of Interest (COI)

Disclose if any of:
- You work at the same company as the reviewer
- You collaborated with the reviewer in the last 2 years
- You are family with the reviewer
- The reviewer is your advisor (or was)

**When reviewing others' work:** Same rules apply — recuse yourself if you have a COI.

### 6. Data With Human Subjects

If your research involves **people** (surveys, interviews, behavior, medical data):

- ✅ Get **IRB / ethics committee** approval (your university has one)
- ✅ Get **informed consent** in writing
- ✅ Anonymize / pseudonymize
- ✅ Allow people to **withdraw** at any time
- ✅ Store data securely (encrypted, access-controlled)
- ✅ Keep data only as long as needed (GDPR: justified retention)

### 7. The 7 Deadly Sins Of Research

| Sin | What It Is | Why It's Bad |
|---|---|---|
| Fabrication | Making up data | Career-ending |
| Falsification | Changing data to fit hypothesis | Career-ending |
| Plagiarism | Copying without citation | Career-ending |
| Self-plagiarism | Re-using your own work | Sometimes OK, sometimes not |
| Salami slicing | 1 paper → 5 thin papers | Disliked, but not always wrong |
| Gift authorship | Adding a name that did nothing | Misrepresents credit |
| Ghost authorship | Hiding the real author | Misrepresents credit |

### 8. AI Ethics (specifically for you)

**Allowed:**
- Brainstorming, explaining concepts, grammar checking
- Writing boilerplate code that you then read and modify
- Translating your own text
- Summarizing papers (read the summary, cite the paper)

**Not allowed (in most journals/conferences):**
- Generating the whole paper text
- Generating fake references
- Submitting AI-generated code without review
- Hiding AI use

**Always:** Disclose AI use in your methods section, like:
> "We used [ChatGPT/Claude] for [X] in [stage]. All output was reviewed and edited by the authors."

**Check** your target venue's policy. They are increasingly strict.

## 📚 Citation Cheat Sheet

### APA (7th edition) — Psychology, Education
```
Smith, J., & Lee, A. (2024). Title of paper. Journal Name, 12(3), 45-67.
https://doi.org/10.xxxx
```

### IEEE — Engineering, CS
```
[1] J. Smith and A. Lee, "Title of paper," Journal Name, vol. 12, no. 3,
    pp. 45-67, 2024, doi: 10.xxxx.
```

### ACM — Computing
```
[1] John Smith and Alice Lee. 2024. Title of paper. Journal Name 12, 3,
    Article 4 (March 2024), 23 pages. https://doi.org/10.xxxx
```

### BibTeX (use with LaTeX)
```bibtex
@article{smith2024title,
  author  = {Smith, John and Lee, Alice},
  title   = {Title of paper},
  journal = {Journal Name},
  year    = {2024},
  volume  = {12},
  number  = {3},
  pages   = {45--67},
  doi     = {10.xxxx}
}
```

### Quick tools
- **Zotero** (free) — auto-extract citations from PDFs
- **Google Scholar "Cite"** — copy a ready-made citation
- **DOI.org** — paste a DOI to get the full metadata
- **Crossref API** — programmatic citation lookup

## ✅ Advanced "Done When"

- [ ] You can name the 3 types of algorithmic bias
- [ ] You know the CRediT taxonomy for authorship
- [ ] You can detect fairness issues in your model
- [ ] You can write a citation in APA, IEEE, and ACM
- [ ] You know your IRB process (if using human data)
- [ ] You have an AI-use disclosure section ready
