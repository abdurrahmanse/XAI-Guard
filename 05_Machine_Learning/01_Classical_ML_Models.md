# 05 — Machine Learning

> **The ML models you need to know for your thesis.**

---

## 📚 3 Things To Learn

| # | Topic | Time |
|---|---|---|
| 01 | Classical ML models | 3 weeks |
| 02 | Deep learning basics | 2 weeks |
| 03 | Model evaluation & tuning | 1 week |

---

## 01. Classical ML Models

**Most important models:**

| Model | Use Case |
|---|---|
| Linear regression | Predict numbers |
| Logistic regression | Yes/No classification |
| Decision tree | Easy to understand |
| Random Forest | Strong baseline |
| XGBoost | Best for tabular data |
| SVM | Complex boundaries |

**Quick start:**

```python
from sklearn.ensemble import RandomForestClassifier
model = RandomForestClassifier()
model.fit(X_train, y_train)
print(model.score(X_test, y_test))
```

**Best book:** Hands-On Machine Learning (Géron)

---

## 02. Deep Learning Basics

**You need to know:**

| Architecture | Use Case |
|---|---|
| ANN / MLP | Tabular data |
| CNN | Images |
| RNN / LSTM | Sequences |
| Transformer | Text, modern AI |

**Simple PyTorch example:**

```python
import torch
import torch.nn as nn

model = nn.Sequential(
    nn.Linear(10, 64),
    nn.ReLU(),
    nn.Linear(64, 1)
)
```

**Resources:**
- fast.ai course (free)
- PyTorch tutorials

---

## 03. Model Evaluation & Tuning

**Always check:**

| Metric | For |
|---|---|
| Accuracy | Balanced classes |
| Precision/Recall | Imbalanced data |
| F1-score | Balance precision & recall |
| AUC-ROC | Threshold-independent |
| MAE / RMSE | Regression |

**Cross-validation:**

```python
from sklearn.model_selection import cross_val_score
scores = cross_val_score(model, X, y, cv=5)
```

**Hyperparameter tuning:**

```python
from sklearn.model_selection import GridSearchCV
grid = GridSearchCV(model, params, cv=5)
grid.fit(X_train, y_train)
```

---

## ✅ Done When

- [ ] You trained 5+ ML models
- [ ] You built a neural network
- [ ] You compared models with metrics
- [ ] You tuned hyperparameters
