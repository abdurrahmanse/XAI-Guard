# 02 — EDA & Visualization

> **Look at your data BEFORE you model. Always.**

---

## What Is EDA?

**EDA = Exploratory Data Analysis**

It's looking at your data carefully before you do anything fancy.

**Goal:** Find patterns, errors, and interesting things.

---

## The 5 Things To Always Check

### 1. Shape
```python
print(df.shape)  # how many rows and columns?
```

### 2. Types
```python
print(df.dtypes)  # what's a number, what's text?
```

### 3. Missing Values
```python
print(df.isnull().sum())
```

### 4. Summary Stats
```python
print(df.describe())
```

### 5. Distribution
```python
import matplotlib.pyplot as plt
df['column'].hist()
plt.show()
```

---

## Chart Cheat Sheet

| Goal | Chart | Code |
|---|---|---|
| Compare numbers | Bar | `df.plot.bar()` |
| Distribution | Histogram | `df.hist()` |
| Box plot | Show spread | `df.boxplot()` |
| Relationship | Scatter | `plt.scatter(x, y)` |
| Time | Line | `df.plot.line()` |
| Correlation | Heatmap | `sns.heatmap(df.corr())` |

---

## Common Findings In EDA

- 🚨 Missing values (decide what to do)
- 🚨 Outliers (very big or very small)
- 🚨 Class imbalance (90% one class)
- 🚨 Weird distributions (try log/sqrt)
- 🚨 Strong correlations (redundant features)
- ✅ Surprising patterns (write them down!)

---

## Tools

| Tool | Use |
|---|---|
| Pandas | Tables, stats |
| Matplotlib | Basic charts |
| Seaborn | Pretty statistical charts |
| Plotly | Interactive charts |
| pandas-profiling | Auto EDA report |

---

## ✅ Done When

- [ ] You made 5+ charts
- [ ] You found 3+ insights
- [ ] You wrote a 1-page EDA report
- [ ] You used seaborn heatmap
