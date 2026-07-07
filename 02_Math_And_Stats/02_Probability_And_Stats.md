# 02 — Probability & Statistics

> **The heart of data science. Master this.**

---

## 1. Descriptive Statistics

| Term | Meaning | Formula |
|---|---|---|
| Mean | Average | sum / count |
| Median | Middle value | sort, pick middle |
| Mode | Most common | most frequent |
| Std dev | Spread | √(variance) |
| Variance | Squared spread | mean of (x - mean)² |

---

## 2. Probability Basics

| Term | Meaning |
|---|---|
| P(A) | Chance of A happening |
| P(A and B) | Both happen |
| P(A or B) | At least one |
| P(A\|B) | A given B happened |

**Bayes Theorem:**
```
P(A|B) = P(B|A) × P(A) / P(B)
```

---

## 3. Common Distributions

| Distribution | When To Use | Shape |
|---|---|---|
| Normal | Heights, weights | Bell curve |
| Binomial | Yes/No, n times | Bars |
| Poisson | Counts in time | Skewed |
| Uniform | All equally likely | Flat |

---

## 4. Central Limit Theorem

**The magic rule:**
If you take many samples and plot their means, you get a **normal distribution** — even if the original data isn't normal!

This is why we can use normal-based tests.

---

## 5. Confidence Intervals

**"We are 95% sure the true mean is in this range."**

Example: The average height is 170 cm ± 3 cm (95% CI)

---

## 6. Correlation vs Causation

**Correlation ≠ Causation**

- Correlation: A and B move together
- Causation: A causes B

Ice cream sales ↑ AND drowning deaths ↑ (because of summer, not because ice cream causes drowning)

---

## ✏️ Practice Exercises

### Exercise 1: Calculate Mean, Median, Mode (Easy)
**Time:** 30 minutes
**Task:** Calculate statistics for a dataset.
**Why:** These are the most basic stats you'll use every day.

**Data:** [12, 15, 18, 22, 22, 25, 30, 30, 30, 35]

**By hand:**
- Mean = (12+15+18+22+22+25+30+30+30+35) / 10 = 239/10 = **23.9**
- Median = (22+25)/2 = **23.5**
- Mode = **30** (appears 3 times)
- Min = 12, Max = 35
- Range = 35 - 12 = 23

**In Python:**
```python
import numpy as np
from scipy import stats

data = [12, 15, 18, 22, 22, 25, 30, 30, 30, 35]
print("Mean:", np.mean(data))
print("Median:", np.median(data))
print("Mode:", stats.mode(data))
print("Std:", np.std(data))
print("Min:", np.min(data), "Max:", np.max(data))
```

---

### Exercise 2: Standard Deviation & Variance (Easy)
**Time:** 30 minutes
**Task:** Calculate std and variance.
**Why:** They tell you how spread out your data is.

**Data:** [4, 8, 6, 5, 3, 8, 9, 2]

**By hand:**
1. Mean = 5.375
2. Differences: [-1.375, 2.625, 0.625, -0.375, -2.375, 2.625, 3.625, -3.375]
3. Squared: [1.89, 6.89, 0.39, 0.14, 5.64, 6.89, 13.14, 11.39]
4. Sum = 46.37
5. Variance = 46.37 / 8 = 5.80
6. Std = √5.80 ≈ **2.41**

**In Python:**
```python
import numpy as np
data = [4, 8, 6, 5, 3, 8, 9, 2]
print("Variance:", np.var(data))
print("Std:", np.std(data))
```

---

### Exercise 3: Probability Calculations (Easy)
**Time:** 30 minutes
**Task:** Solve basic probability problems.
**Why:** You need this for hypothesis testing.

**Questions:**

**Q1:** Roll a die. P(rolling a 4)?
- Answer: 1/6 ≈ 0.167

**Q2:** Toss 2 coins. P(both heads)?
- P(H1) × P(H2) = 0.5 × 0.5 = 0.25

**Q3:** Draw 1 card from deck. P(ace OR king)?
- P(ace) = 4/52, P(king) = 4/52
- P(ace or king) = 8/52 = 2/13 ≈ 0.154

**Q4:** 1% of people have a disease. Test is 99% accurate. If positive, what's the chance you have it?
- P(disease) = 0.01
- P(positive | disease) = 0.99
- P(positive | no disease) = 0.01
- P(positive) = 0.99 × 0.01 + 0.01 × 0.99 = 0.0198
- P(disease | positive) = (0.99 × 0.01) / 0.0198 ≈ **0.5 (50%)**

This is Bayes' theorem in action!

**In Python:**
```python
from fractions import Fraction
print(Fraction(1, 6))  # Q1
print(Fraction(1, 4))  # Q2
print(Fraction(8, 52)) # Q3
```

---

### Exercise 4: Generate Random Samples (Medium)
**Time:** 1 hour
**Task:** Simulate dice rolls and coin flips.
**Why:** Understand randomness through simulation.

```python
import numpy as np

# Flip a coin 1000 times
flips = np.random.choice(['H', 'T'], size=1000)
heads = sum(flips == 'H')
print(f"Heads: {heads} ({heads/10}%)")  # Should be near 50%

# Roll a die 1000 times
rolls = np.random.randint(1, 7, size=1000)
print(f"Average: {rolls.mean()}")  # Should be near 3.5

# Plot histogram
import matplotlib.pyplot as plt
plt.hist(rolls, bins=6)
plt.title("1000 dice rolls")
plt.show()
```

**Try:** Generate 10,000 samples. The average gets closer to 3.5.

---

### Exercise 5: Central Limit Theorem In Action (Hard but amazing)
**Time:** 1-2 hours
**Task:** Show the Central Limit Theorem visually.
**Why:** This is one of the most important ideas in statistics.

```python
import numpy as np
import matplotlib.pyplot as plt

# Take 10,000 samples of size 30 from uniform distribution
sample_means = []
for _ in range(10000):
    sample = np.random.uniform(0, 1, size=30)
    sample_means.append(sample.mean())

# Plot histogram
plt.hist(sample_means, bins=50, edgecolor='black')
plt.title("Distribution of sample means (n=30)")
plt.xlabel("Sample mean")
plt.ylabel("Count")
plt.show()
```

**You'll see a bell curve**, even though the original was uniform!

**Try:** Change n to 5, 30, 100. See how it changes.

---

### Exercise 6: Bayesian Updating (Hard)
**Time:** 1-2 hours
**Task:** Build a simple spam filter using Bayes' theorem.
**Why:** Real-world application of probability.

**Setup:** You have 100 emails. 30 are spam. In spam, 80% have "offer". In non-spam, 10% have "offer".

**Question:** Email has "offer". What's P(spam)?

**Bayes:**
P(spam | offer) = P(offer | spam) × P(spam) / P(offer)

P(offer) = P(offer|spam) × P(spam) + P(offer|not spam) × P(not spam)
P(offer) = 0.8 × 0.3 + 0.1 × 0.7 = 0.24 + 0.07 = 0.31

P(spam | offer) = 0.8 × 0.3 / 0.31 = **0.77 (77%)**

**In Python:**
```python
def bayes(p_a, p_b_given_a, p_b_given_not_a):
    p_not_a = 1 - p_a
    p_b = p_b_given_a * p_a + p_b_given_not_a * p_not_a
    return (p_b_given_a * p_a) / p_b

p_spam = bayes(0.3, 0.8, 0.1)
print(f"P(spam | offer) = {p_spam:.2%}")
```

---

## ✅ Done When

- [ ] You can calculate mean, std, variance
- [ ] You can apply Bayes theorem
- [ ] You know 4 common distributions
- [ ] You understand confidence intervals
- [ ] You completed all 6 exercises
