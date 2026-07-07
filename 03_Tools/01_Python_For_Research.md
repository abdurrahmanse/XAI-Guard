# 01 — Python For Research

> **Key libraries: NumPy, Pandas, Matplotlib, Scikit-learn, PyTorch**

---

## 1. NumPy (Numerical Computing)

**What:** Fast math on arrays. Foundation of all ML.

```python
import numpy as np

# Create arrays
a = np.array([1, 2, 3])
b = np.array([[1, 2], [3, 4]])

# Operations
a + 10           # [11, 12, 13]
a * 2            # [2, 4, 6]
a.mean()         # 2.0
a.reshape(3, 1)  # change shape
```

---

## 2. Pandas (Tabular Data)

**What:** Work with tables (like Excel, but better).

```python
import pandas as pd

df = pd.read_csv("data.csv")
df.head()         # first 5 rows
df.info()         # column types
df.describe()     # statistics
df["age"].mean()  # mean of one column
df[df["age"] > 30]  # filter
```

---

## 3. Matplotlib (Charts)

```python
import matplotlib.pyplot as plt
plt.plot([1, 2, 3], [4, 5, 6])
plt.xlabel("X")
plt.ylabel("Y")
plt.title("My Chart")
plt.show()
```

---

## 4. Scikit-learn (ML)

```python
from sklearn.ensemble import RandomForestClassifier
model = RandomForestClassifier()
model.fit(X_train, y_train)
print(model.score(X_test, y_test))
```

---

## 5. PyTorch (Deep Learning)

```python
import torch
import torch.nn as nn
model = nn.Linear(10, 1)
```

---

## Where To Practice

| Resource | Use |
|---|---|
| Kaggle Learn | Free mini-courses |
| Kaggle Competitions | Real datasets |
| Google Colab | Free Python + GPU |

---

## ✏️ Practice Exercises

### Exercise 1: NumPy Basics (Easy)
**Time:** 1-2 hours
**Task:** Do 10 NumPy operations.
**Why:** NumPy is the foundation.

```python
import numpy as np

# 1. Create array from 0 to 9
a = np.arange(10)
print(a)

# 2. Reshape to 2x5
b = a.reshape(2, 5)
print(b)

# 3. All zeros, all ones
print(np.zeros(5))
print(np.ones(5))

# 4. Random numbers
np.random.seed(42)
print(np.random.rand(3))  # uniform [0,1)
print(np.random.randn(3)) # standard normal

# 5. Statistics
print(b.mean(), b.std(), b.sum())

# 6. Indexing & slicing
print(a[3:7])      # elements 3 to 6
print(b[0, :])     # first row
print(b[:, 1])     # second column

# 7. Boolean indexing
print(a[a > 5])    # elements > 5

# 8. Matrix multiplication
A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])
print(A @ B)
print(np.dot(A, B))

# 9. Solving linear system
# 2x + 3y = 8, x - y = 1
A = np.array([[2, 3], [1, -1]])
b = np.array([8, 1])
print(np.linalg.solve(A, b))

# 10. Eigenvalues
eigvals, eigvecs = np.linalg.eig(A)
print(eigvals)
```

---

### Exercise 2: Pandas Data Analysis (Medium)
**Time:** 2-3 hours
**Task:** Analyze a real dataset.
**Why:** You'll do this every day as a researcher.

**Step 1:** Download Titanic dataset from Kaggle.

**Step 2:** Do this analysis:
```python
import pandas as pd
df = pd.read_csv("titanic.csv")

# 1. How many rows and columns?
print(df.shape)

# 2. What are the column types?
print(df.dtypes)

# 3. How many missing values per column?
print(df.isnull().sum())

# 4. Fill missing age with median
df["age"] = df["age"].fillna(df["age"].median())

# 5. Summary statistics
print(df.describe())

# 6. Survival rate by sex
print(df.groupby("sex")["survived"].mean())

# 7. Survival rate by class
print(df.groupby("pclass")["survived"].mean())

# 8. Age distribution
print(df["age"].describe())

# 9. Create new column: is child
df["is_child"] = (df["age"] < 12).astype(int)

# 10. Save cleaned data
df.to_csv("titanic_clean.csv", index=False)
```

**Try:** Group by both sex and class. Who had the highest survival rate?

---

### Exercise 3: Matplotlib Charts (Easy)
**Time:** 1-2 hours
**Task:** Make 6 chart types.
**Why:** Every paper needs good charts.

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 10, 100)

# 1. Line plot
plt.plot(x, np.sin(x))
plt.title("Sine wave")
plt.show()

# 2. Scatter plot
plt.scatter(np.random.rand(50), np.random.rand(50))
plt.title("Random scatter")
plt.show()

# 3. Histogram
plt.hist(np.random.randn(1000), bins=30)
plt.title("Normal distribution")
plt.show()

# 4. Bar chart
plt.bar(["A", "B", "C"], [3, 7, 5])
plt.title("Bar chart")
plt.show()

# 5. Subplots
fig, axes = plt.subplots(1, 2, figsize=(10, 4))
axes[0].plot(x, np.sin(x))
axes[0].set_title("Sine")
axes[1].plot(x, np.cos(x))
axes[1].set_title("Cosine")
plt.show()

# 6. Save as image
plt.plot(x, np.sin(x))
plt.savefig("my_chart.png", dpi=300)
```

**Try:** Use the Titanic dataset to make 5 meaningful charts.

---

### Exercise 4: End-to-End Mini Project (Hard)
**Time:** 4-6 hours
**Task:** Predict Titanic survival.
**Why:** This is the classic beginner project.

```python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# 1. Load data
df = pd.read_csv("titanic.csv")

# 2. Clean
df["age"] = df["age"].fillna(df["age"].median())
df["embarked"] = df["embarked"].fillna("S")
df = pd.get_dummies(df, columns=["sex", "embarked"])

# 3. Features & target
X = df[["pclass", "age", "fare", "sex_female", "sex_male"]]
y = df["survived"]

# 4. Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 5. Train
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 6. Evaluate
y_pred = model.predict(X_test)
print(f"Accuracy: {accuracy_score(y_test, y_pred):.2%}")

# 7. Feature importance
import matplotlib.pyplot as plt
importance = pd.Series(model.feature_importances_, index=X.columns)
importance.sort_values().plot.barh()
plt.title("Feature importance")
plt.show()
```

**Try:** Beat 80% accuracy. Try XGBoost.

---

### Exercise 5: Kaggle Mini Competition (Hard)
**Time:** 1 week
**Task:** Enter any Kaggle beginner competition.
**Why:** Real-world practice.

**Recommended for beginners:**
- Titanic (binary classification)
- House Prices (regression)
- Digit Recognizer (image classification)

**Steps:**
1. Sign up at kaggle.com (free)
2. Pick a competition
3. Read the "Getting Started" notebook
4. Submit a simple version
5. Iterate

---

## ✅ Done When

- [ ] You can use NumPy and Pandas
- [ ] You can make 5+ chart types
- [ ] You completed the Titanic mini-project
- [ ] You pushed code to GitHub
- [ ] You completed all 5 exercises
