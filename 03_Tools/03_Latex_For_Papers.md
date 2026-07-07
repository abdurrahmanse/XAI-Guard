# 03 — LaTeX For Papers

> **All research papers are written in LaTeX. Learn the basics.**

---

## Why LaTeX?

- Looks professional
- Handles math perfectly
- Used by all journals
- Free!

---

## Easy Way To Start: Overleaf

Go to **overleaf.com** (free account)

- Online editor
- No installation
- Many templates
- Auto-saves your work

---

## The Simplest Document

```latex
\documentclass{article}
\title{My Research}
\author{Your Name}
\date{\today}

\begin{document}
\maketitle

\section{Introduction}
This is my research.

\section{Methods}
I used Python.

\section{Results}
It worked.

\end{document}
```

---

## Useful Things

### Math
```latex
Inline: $E = mc^2$
Display: $$\sum_{i=1}^{n} x_i$$
```

### Figure
```latex
\begin{figure}
  \includegraphics[width=0.8\textwidth]{my_chart.png}
  \caption{My results}
\end{figure}
```

### Table
```latex
\begin{table}
  \begin{tabular}{ll}
    A & B \\
    C & D
  \end{tabular}
\end{table}
```

### Citation
```latex
According to Smith et al. \cite{smith2023}, ...
```

---

## IMRaD Template

Search "IMRaD template" in Overleaf gallery.
Pick one, fill it in.

---

## ✏️ Practice Exercises

### Exercise 1: First LaTeX Document (Easy)
**Time:** 1 hour
**Task:** Write your first LaTeX doc on Overleaf.
**Why:** Get familiar with the editor.

**Steps:**
1. Go to overleaf.com, sign up (free)
2. Click "New Project" → "Blank Paper"
3. Replace the code with:

```latex
\documentclass{article}
\usepackage[utf8]{inputenc}
\usepackage{amsmath}
\title{My First Paper}
\author{Your Name}
\date{\today}

\begin{document}
\maketitle

\section{Introduction}
This is my first \LaTeX{} document.
I am learning to write like a researcher.

\section{Methods}
I used Google and Overleaf.

\section{Results}
It worked! See Equation~\ref{eq:1}.

\begin{equation}
E = mc^2
\label{eq:1}
\end{equation}

\section{Conclusion}
LaTeX is fun.

\end{document}
```

4. Click "Recompile"
5. You should see a PDF! 🎉

---

### Exercise 2: Add Math Equations (Easy)
**Time:** 1 hour
**Task:** Write 5 different math equations.
**Why:** Math is everywhere in research.

**Try these:**

```latex
% Inline math
The mean is $\mu = \frac{1}{n}\sum_{i=1}^{n} x_i$.

% Display math
\[
\sigma = \sqrt{\frac{1}{n}\sum_{i=1}^{n}(x_i - \mu)^2}
\]

% Aligned equations
\begin{align}
f(x) &= ax^2 + bx + c \\
f'(x) &= 2ax + b \\
f''(x) &= 2a
\end{align}

% Matrices
\[
A = \begin{pmatrix}
1 & 2 \\
3 & 4
\end{pmatrix}
\]

% Greek letters
$\alpha, \beta, \gamma, \delta, \theta, \lambda, \mu, \sigma$
```

**Try:** Write the linear regression equation in LaTeX.

---

### Exercise 3: Insert A Figure (Easy)
**Time:** 30 minutes
**Task:** Add a chart to your LaTeX doc.
**Why:** Every paper needs figures.

**Steps:**
1. Make a chart in Python and save as PNG
2. In Overleaf, click the upload icon (top left)
3. Upload your image
4. Add this code to your doc:

```latex
\begin{figure}[h]
  \centering
  \includegraphics[width=0.7\textwidth]{my_chart.png}
  \caption{This is my amazing result.}
  \label{fig:result}
\end{figure}
```

5. Reference it in text: "As shown in Figure~\ref{fig:result}..."

**Try:** Add 3 different charts to a single doc.

---

### Exercise 4: Make A Table (Easy)
**Time:** 30 minutes
**Task:** Create a results table.
**Why:** Tables are clearer than text for comparisons.

**Sample code:**

```latex
\begin{table}[h]
  \centering
  \caption{Comparison of methods on the test dataset.}
  \label{tab:results}
  \begin{tabular}{|l|c|c|c|}
    \hline
    Method & Accuracy & Precision & Recall \\
    \hline
    Logistic Regression & 0.78 & 0.75 & 0.80 \\
    Random Forest & 0.85 & 0.83 & 0.86 \\
    XGBoost & 0.89 & 0.88 & 0.90 \\
    \hline
  \end{tabular}
\end{table}
```

**Try:** Add a comparison table from your own analysis.

---

### Exercise 5: Use An IMRaD Template (Medium)
**Time:** 2 hours
**Task:** Find and use a real research paper template.
**Why:** Your thesis and papers will use these.

**Steps:**
1. Go to Overleaf Gallery: overleaf.com/gallery
2. Search "IMRaD" or "research paper"
3. Pick a template (try "IEEE conference" or "NeurIPS")
4. Open it
5. Fill in your info:
   - Title
   - Author
   - Abstract
   - Each section
6. Recompile to see the result

**Tip:** Don't fight the template. Just fill in your content.

---

### Exercise 6: Add Citations (Medium)
**Time:** 1 hour
**Task:** Cite 3 papers properly.
**Why:** Every paper needs references.

**Steps:**
1. In Overleaf, click "New File" → name it `references.bib`
2. Add 3 references in BibTeX format:

```bibtex
@article{smith2024,
  author = {John Smith},
  title = {A new method for machine learning},
  journal = {Nature Machine Intelligence},
  year = {2024},
  volume = {6},
  pages = {1--10}
}

@inproceedings{lee2023,
  author = {Jane Lee and Bob Park},
  title = {Deep learning for image classification},
  booktitle = {Proceedings of CVPR},
  year = {2023}
}

@book{goodfellow2016,
  author = {Ian Goodfellow and Yoshua Bengio and Aaron Courville},
  title = {Deep Learning},
  publisher = {MIT Press},
  year = {2016}
}
```

3. Cite in your paper: `\cite{smith2024}`
4. Add bibliography at end: `\bibliography{references}` or `\printbibliography`

**Try:** Use Zotero to auto-generate BibTeX entries from Google Scholar.

---

### Exercise 7: Write A 2-Page Paper (Hard)
**Time:** 4-6 hours
**Task:** Write a complete mini research paper.
**Why:** This is the real practice.

**Pick a topic.** It can be simple. Example:
- "Comparing 3 ML algorithms on the Iris dataset"

**Use this structure:**
- Title
- Abstract (100 words)
- Introduction (1 paragraph)
- Methods (1 paragraph)
- Results (table + figure)
- Discussion (1 paragraph)
- Conclusion (1 paragraph)
- References (3-5)

**Use the IMRaD template from Overleaf.**

---

## ✅ Done When

- [ ] You wrote a 1-page LaTeX doc
- [ ] You used an IMRaD template
- [ ] You added a figure, table, and equation
- [ ] You cited a paper
- [ ] You wrote a 2-page paper
- [ ] You completed all 7 exercises
