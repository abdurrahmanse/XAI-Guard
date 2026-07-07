# 03 — Model Evaluation & Tuning

> **How to know if your model is actually good.**

---

## The Golden Rule

**Never test on the data you trained on!**

Split your data:
- **Train:** 70% (teach the model)
- **Validation:** 15% (tune the model)
- **Test:** 15% (final check, use ONCE)

---

## Classification Metrics

| Metric | When | Formula |
|---|---|---|
| Accuracy | Balanced | Correct / Total |
| Precision | Cost of FP high | TP / (TP + FP) |
| Recall | Cost of FN high | TP / (TP + FN) |
| F1 | Balance | 2 × P × R / (P + R) |
| AUC-ROC | General | Area under curve |

**Tip:** If classes are imbalanced, don't use accuracy!

---

## Regression Metrics

| Metric | Meaning |
|---|---|
| MAE | Average error |
| MSE | Squared error (punishes big errors) |
| RMSE | Same unit as target |
| R² | Variance explained (0-1) |

---

## Cross-Validation

Train on 4 parts, test on 1 part. Repeat 5 times.

```python
from sklearn.model_selection import cross_val_score
scores = cross_val_score(model, X, y, cv=5)
print(f"Average: {scores.mean():.3f}")
```

**Why?** More reliable than single train/test split.

---

## Hyperparameter Tuning

### Grid Search
Try all combinations. Slow but thorough.

```python
from sklearn.model_selection import GridSearchCV
params = {'n_estimators': [50, 100, 200]}
grid = GridSearchCV(model, params, cv=5)
grid.fit(X_train, y_train)
print(grid.best_params_)
```

### Random Search
Try random combinations. Faster.

### Bayesian (Optuna)
Smart search. Best for expensive models.

---

## Common Pitfalls

❌ **Data leakage:** Using test data in training
❌ **Overfitting:** Model memorizes training data
❌ **Wrong metric:** Using accuracy on imbalanced data
❌ **No baseline:** Don't compare against simple models
❌ **Ignoring variance:** Run multiple seeds

---

## ✅ Done When

- [ ] You used train/val/test split
- [ ] You used cross-validation
- [ ] You compared 2+ models
- [ ] You tuned hyperparameters
- [ ] You reported the right metric
