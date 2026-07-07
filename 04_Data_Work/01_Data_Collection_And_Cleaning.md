# 04 — Data Work

> **How to find, clean, and prepare data for your research.**

---

## 📚 3 Things To Learn

| # | Topic | Time |
|---|---|---|
| 01 | Data collection & cleaning | 1 week |
| 02 | EDA & visualization | 1 week |
| 03 | Feature engineering | 1 week |

---

## 01. Data Collection & Cleaning

**Where to find data:**
- Kaggle.com
- UCI Machine Learning Repository
- data.gov
- Google Dataset Search
- APIs (Twitter, weather, etc.)

**Cleaning steps:**
1. Check for missing values
2. Handle outliers
3. Fix data types
4. Remove duplicates

**Code example:**

```python
import pandas as pd
df = pd.read_csv("data.csv")
print(df.isnull().sum())  # check missing
df = df.dropna()  # remove missing
```

---

## 02. EDA & Visualization

**EDA = Exploratory Data Analysis**

**Always ask:**
- What's the shape? (rows, columns)
- What are the data types?
- Are there missing values?
- What's the distribution?
- Are variables correlated?

**Chart types:**

| Goal | Chart |
|---|---|
| Compare values | Bar chart |
| Distribution | Histogram, box plot |
| Relationship | Scatter plot |
| Time | Line chart |
| Correlation | Heatmap |

**Tool:** Matplotlib, Seaborn, Plotly

---

## 03. Feature Engineering

**Create new features from existing data:**

| Type | Example |
|---|---|
| Date | Extract day, month, year |
| Text | Length, word count |
| Math | Ratios, differences |
| Bins | Age → young/old |

**Encode categories:**

```python
df = pd.get_dummies(df, columns=['category'])
```

**Scale numbers:**

```python
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
```

---

## ✅ Done When

- [ ] You can find and load data
- [ ] You cleaned a messy dataset
- [ ] You made 5+ charts
- [ ] You created 3+ new features
