# 03 — Feature Engineering

> **Better features = better models. Always.**

---

## What Is Feature Engineering?

It's creating **new useful columns** from existing ones.

Example: From "date of birth", you can create "age", "birth month", "is birthday this week".

---

## 3 Common Techniques

### 1. Date Features
```python
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month
df['day_of_week'] = df['date'].dt.dayofweek
```

### 2. Text Features
```python
df['text_length'] = df['text'].str.len()
df['word_count'] = df['text'].str.split().str.len()
```

### 3. Math Features
```python
df['ratio'] = df['a'] / df['b']
df['log'] = np.log(df['value'])
```

---

## Encoding Categories

ML models need numbers, not text.

| Method | Use | Code |
|---|---|---|
| Label encoding | Ordinal (low, med, high) | `LabelEncoder` |
| One-hot | Nominal (red, blue) | `pd.get_dummies()` |

```python
# One-hot encoding
df = pd.get_dummies(df, columns=['color'])
```

---

## Scaling Numbers

Models work better when numbers are on the same scale.

| Method | When |
|---|---|
| StandardScaler | Normal data (mean 0, std 1) |
| MinMaxScaler | Need values 0-1 |
| RobustScaler | Has outliers |

```python
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
```

---

## Feature Selection

Don't use all features. Pick the best ones.

**3 simple ways:**
1. **Correlation:** Drop features correlated with each other
2. **Tree importance:** Use Random Forest to rank
3. **Lasso:** Use L1 regularization

---

## ✅ Done When

- [ ] You created 3+ new features
- [ ] You encoded categories
- [ ] You scaled numbers
- [ ] You selected top features
