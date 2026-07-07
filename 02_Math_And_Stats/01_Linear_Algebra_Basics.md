# 01 — Linear Algebra Basics

> **The math you need for Data Science research.**

---

## 📚 3 Things To Learn

| # | Topic | Time |
|---|---|---|
| 01 | Linear algebra basics | 1 week |
| 02 | Probability & statistics | 2 weeks |
| 03 | Hypothesis testing | 1 week |

---

## 01. Linear Algebra Basics

**You need to know:**

| Concept | Simple Meaning |
|---|---|
| Vector | A list of numbers [1, 2, 3] |
| Matrix | A 2D list of numbers |
| Dot product | Multiply and add: a·b = a₁b₁ + a₂b₂ |
| Eigenvalue | Special number for transformation |

**Resources:**
- 3Blue1Brown YouTube: "Essence of Linear Algebra"
- Khan Academy: Linear Algebra

---

## ✏️ Practice Exercises

### Exercise 1: Vector Operations (Easy)
**Time:** 1 hour
**Task:** Do basic vector math by hand and in Python.
**Why:** Vectors are everywhere in ML.

**By hand:**
Given: a = [2, 3, 1], b = [1, 0, 4]

Calculate:
1. a + b = ?
2. a - b = ?
3. 3 × a = ?
4. a · b (dot product) = ?
5. ||a|| (length/magnitude) = ?

**Answers:**
1. [3, 3, 5]
2. [1, 3, -3]
3. [6, 9, 3]
4. (2×1) + (3×0) + (1×4) = 6
5. √(4+9+1) = √14 ≈ 3.74

**In Python:**
```python
import numpy as np
a = np.array([2, 3, 1])
b = np.array([1, 0, 4])
print(a + b)        # [3 3 5]
print(a - b)        # [1 3 -3]
print(3 * a)        # [6 9 3]
print(np.dot(a, b)) # 6
print(np.linalg.norm(a))  # 3.74
```

---

### Exercise 2: Matrix Multiplication (Medium)
**Time:** 1 hour
**Task:** Multiply two matrices by hand, then in Python.
**Why:** Neural networks are mostly matrix multiplications.

**By hand:**
Given:
```
A = [1 2]    B = [5 6]
    [3 4]        [7 8]
```

Calculate A × B.

**Answer:**
```
A × B = [(1×5+2×7)  (1×6+2×8)]   = [19 22]
        [(3×5+4×7)  (3×6+4×8)]     [43 50]
```

**In Python:**
```python
import numpy as np
A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])
print(A @ B)
# [[19 22]
#  [43 50]]
```

**Try 5 more:** Mix 2x2 and 3x3 matrices.

---

### Exercise 3: Solve A System Of Equations (Medium)
**Time:** 1-2 hours
**Task:** Solve 2x + 3y = 8 and x - y = 1.
**Why:** Linear regression = solving such systems.

**Math:**
```
2x + 3y = 8
x - y = 1
```

From eq 2: x = 1 + y
Substitute: 2(1+y) + 3y = 8 → 2 + 5y = 8 → y = 6/5 = 1.2
x = 1 + 1.2 = 2.2

**Answer:** x = 2.2, y = 1.2

**In Python:**
```python
import numpy as np
A = np.array([[2, 3], [1, -1]])
b = np.array([8, 1])
x = np.linalg.solve(A, b)
print(x)  # [2.2 1.2]
```

**Try 3 more:** 2x2 systems.

---

### Exercise 4: PCA By Hand (Hard but powerful)
**Time:** 2-3 hours
**Task:** Do PCA on a 2D dataset to find the main direction.
**Why:** PCA is used everywhere (dimensionality reduction, visualization).

**Steps:**
1. Center the data (subtract mean)
2. Calculate covariance matrix
3. Find eigenvalues and eigenvectors
4. Top eigenvector = main direction

**Sample data (heights, weights):**
```python
import numpy as np
X = np.array([[170, 65], [180, 75], [160, 55], [175, 70]])
X_centered = X - X.mean(axis=0)
cov = np.cov(X_centered.T)
eigenvalues, eigenvectors = np.linalg.eig(cov)
print("Eigenvalues:", eigenvalues)
print("Main direction:", eigenvectors[:, 0])
```

**Try this:** Plot the data and the main direction. You should see that height and weight are correlated.

---

### Exercise 5: Implement Linear Regression From Scratch (Hard)
**Time:** 3-4 hours
**Task:** Build linear regression using ONLY linear algebra (no sklearn).
**Why:** This is THE exercise. It connects everything.

**The math:**
y = X × w + b

Where:
- X = inputs (n × m)
- w = weights (m × 1)
- b = bias

**Solution using Normal Equation:**
w = (XᵀX)⁻¹ Xᵀy

**Code:**
```python
import numpy as np

# Data
X = np.array([[1], [2], [3], [4], [5]])
y = np.array([2, 4, 5, 4, 5])

# Add bias column
X_b = np.c_[np.ones((5, 1)), X]

# Normal equation
theta = np.linalg.inv(X_b.T @ X_b) @ X_b.T @ y
print("Weights:", theta)  # [intercept, slope]

# Predict
y_pred = X_b @ theta
print("Predictions:", y_pred)
```

**Compare with sklearn:**
```python
from sklearn.linear_model import LinearRegression
model = LinearRegression()
model.fit(X, y)
print("sklearn weights:", model.intercept_, model.coef_)
```

**They should match!**

---

## ✅ Done When

- [ ] You can do matrix multiplication
- [ ] You understand normal distribution
- [ ] You can run a t-test
- [ ] You can explain p-value to a friend
- [ ] You completed all 5 exercises
