# 03 — Hypothesis Testing

> **How to know if your result is real or just luck.**

---

## The Basic Idea

You have two options:
- **H₀ (null hypothesis):** Nothing is happening (no effect)
- **H₁ (alternative):** Something IS happening (effect exists)

You test the data. If it's very unlikely under H₀, you reject H₀.

---

## Step By Step

1. State H₀ and H₁
2. Pick a significance level: α = 0.05 (5%)
3. Calculate test statistic
4. Calculate p-value
5. Compare p-value to α
6. Decision: Reject H₀ or not

**Rule:** If p-value < 0.05, reject H₀

---

## Common Tests

| Test | Use Case | Python Code |
|---|---|---|
| 1-sample t-test | Compare mean to a value | `scipy.stats.ttest_1samp` |
| 2-sample t-test | Compare 2 groups | `scipy.stats.ttest_ind` |
| Paired t-test | Same group, before/after | `scipy.stats.ttest_rel` |
| Chi-square | Categorical data | `scipy.stats.chi2_contingency` |
| ANOVA | Compare 3+ groups | `scipy.stats.f_oneway` |

---

## Example

**Question:** Do males weigh more than females?

```python
from scipy import stats
t, p = stats.ttest_ind(male_weights, female_weights)
if p < 0.05:
    print("Yes, there's a difference!")
```

---

## Type I vs Type II Error

| | H₀ True | H₀ False |
|---|---|---|
| Reject H₀ | Type I (False alarm) | ✅ Correct |
| Don't Reject | ✅ Correct | Type II (Missed it) |

- Type I: You said there's an effect, but there isn't
- Type II: There IS an effect, but you missed it

---

## Effect Size

p-value tells you IF there's an effect.
Effect size tells you HOW BIG it is.

**Cohen's d:**
- 0.2 = small
- 0.5 = medium
- 0.8 = large

---

## ✏️ Practice Exercises

### Exercise 1: Understand p-value With Coins (Easy)
**Time:** 30 minutes
**Task:** Flip coins to understand p-value.
**Why:** p-value is hard. Practice with simple examples.

**Setup:** You flip a coin 10 times. You get 8 heads.

**Question:** Is the coin fair?

**H₀:** The coin is fair (P(heads) = 0.5)
**H₁:** The coin is biased

**By hand:** If fair, P(8 or more heads) = 0.044 (very unlikely!)

**In Python:**
```python
from scipy import stats
# Probability of getting 8 or more heads out of 10
p_value = 1 - stats.binom.cdf(7, 10, 0.5)
print(f"p-value: {p_value:.4f}")
# If p < 0.05, the coin is probably biased
```

**Try:** Get 7 heads (p = 0.17, not significant) vs 9 heads (p = 0.01, significant).

---

### Exercise 2: 1-Sample t-test (Easy)
**Time:** 30 minutes
**Task:** Test if a sample mean is different from a known value.
**Why:** Most common test in research.

**Setup:** A factory makes chocolate bars. They should weigh 50g.
You sample 10 bars: [49, 51, 50, 52, 48, 50, 51, 49, 50, 52]

**H₀:** Mean weight = 50g
**H₁:** Mean weight ≠ 50g

```python
from scipy import stats
bars = [49, 51, 50, 52, 48, 50, 51, 49, 50, 52]
t, p = stats.ttest_1samp(bars, 50)
print(f"t = {t:.3f}, p = {p:.3f}")
# If p > 0.05, we can't reject H₀ (weights are OK)
```

**Try:** Add a few outliers (e.g., 70, 30). See how p changes.

---

### Exercise 3: 2-Sample t-test (Medium)
**Time:** 1 hour
**Task:** Compare two groups.
**Why:** "Is group A different from group B?" is the most common question.

**Setup:** Test scores from two classes:
- Class A: [85, 90, 78, 92, 88, 76, 95, 89, 84, 91]
- Class B: [79, 85, 82, 88, 75, 80, 83, 79, 81, 84]

**H₀:** Class A mean = Class B mean
**H₁:** Class A mean ≠ Class B mean

```python
from scipy import stats
class_A = [85, 90, 78, 92, 88, 76, 95, 89, 84, 91]
class_B = [79, 85, 82, 88, 75, 80, 83, 79, 81, 84]
t, p = stats.ttest_ind(class_A, class_B)
print(f"t = {t:.3f}, p = {p:.3f}")

# Effect size (Cohen's d)
import numpy as np
pooled_std = np.sqrt((np.std(class_A)**2 + np.std(class_B)**2) / 2)
d = (np.mean(class_A) - np.mean(class_B)) / pooled_std
print(f"Cohen's d = {d:.3f}")
```

**Try:** Make Class A and Class B more similar. See p increase.

---

### Exercise 4: Chi-Square Test (Medium)
**Time:** 1 hour
**Task:** Test if two categorical variables are related.
**Why:** Common for survey data.

**Setup:** Survey of 200 people: Gender vs Coffee preference

|  | Coffee | Tea | Total |
|---|---|---|---|
| Male | 30 | 50 | 80 |
| Female | 40 | 80 | 120 |
| Total | 70 | 130 | 200 |

**H₀:** Gender and preference are independent

```python
from scipy import stats
import numpy as np
table = np.array([[30, 50], [40, 80]])
chi2, p, dof, expected = stats.chi2_contingency(table)
print(f"chi2 = {chi2:.3f}, p = {p:.3f}")
print("Expected values:")
print(expected)
```

**Try:** Change the numbers. When is p < 0.05?

---

### Exercise 5: ANOVA (Hard)
**Time:** 1-2 hours
**Task:** Compare 3+ groups.
**Why:** When you have more than 2 groups, t-test doesn't work.

**Setup:** Test scores from 3 teaching methods:
- Method A: [85, 90, 78, 92, 88]
- Method B: [79, 85, 82, 88, 75]
- Method C: [92, 95, 89, 94, 91]

```python
from scipy import stats
method_A = [85, 90, 78, 92, 88]
method_B = [79, 85, 82, 88, 75]
method_C = [92, 95, 89, 94, 91]
f, p = stats.f_oneway(method_A, method_B, method_C)
print(f"F = {f:.3f}, p = {p:.3f}")
```

**If p < 0.05:** At least one method is different.
**Next step:** Use Tukey's HSD test to find which one.

```python
from statsmodels.stats.multicomp import pairwise_tukeyhsd
data = method_A + method_B + method_C
groups = ['A']*5 + ['B']*5 + ['C']*5
tukey = pairwise_tukeyhsd(data, groups)
print(tukey)
```

---

### Exercise 6: A/B Test Simulation (Hard but real)
**Time:** 2-3 hours
**Task:** Simulate a real A/B test.
**Why:** Industry standard for product decisions.

**Setup:** Your website has 2 versions.
- Version A: 1000 visitors, 50 conversions (5%)
- Version B: 1000 visitors, 75 conversions (7.5%)

**Question:** Is B better?

```python
from scipy import stats
import numpy as np

# Conversion data
A_conv = 50
A_total = 1000
B_conv = 75
B_total = 1000

# Two-proportion z-test
p_A = A_conv / A_total
p_B = B_conv / B_total
p_pooled = (A_conv + B_conv) / (A_total + B_total)
se = np.sqrt(p_pooled * (1 - p_pooled) * (1/A_total + 1/B_total))
z = (p_B - p_A) / se
p_value = 1 - stats.norm.cdf(z)
print(f"z = {z:.3f}, p = {p_value:.4f}")

# Effect size
lift = (p_B - p_A) / p_A * 100
print(f"Lift: {lift:.1f}%")
```

**Try:** Make A and B closer. See p increase.

---

## ✅ Done When

- [ ] You can run a t-test
- [ ] You understand p-value
- [ ] You know Type I vs Type II
- [ ] You can calculate effect size
- [ ] You completed all 6 exercises
