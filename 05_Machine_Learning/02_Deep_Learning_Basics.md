# 02 — Deep Learning Basics

> **Neural networks for images, text, and more.**

---

## What Is Deep Learning?

A neural network is a function that:
1. Takes inputs
2. Multiplies by weights
3. Adds bias
4. Passes through activation
5. Outputs prediction

Many layers = "deep" learning.

---

## 4 Main Architectures

| Type | Use Case | Example |
|---|---|---|
| **ANN/MLP** | Tabular data | Predict house price |
| **CNN** | Images | Detect tumors |
| **RNN/LSTM** | Sequences | Predict stock |
| **Transformer** | Text, modern AI | GPT, BERT |

---

## Simple PyTorch Example

```python
import torch
import torch.nn as nn

model = nn.Sequential(
    nn.Linear(10, 64),    # input → 64
    nn.ReLU(),            # activation
    nn.Linear(64, 1)      # output
)

# Train
criterion = nn.MSELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
```

---

## CNN For Images

```python
model = nn.Sequential(
    nn.Conv2d(3, 16, 3),   # 3 channels → 16
    nn.ReLU(),
    nn.MaxPool2d(2),
    nn.Flatten(),
    nn.Linear(16*13*13, 10)
)
```

---

## Common Terms

| Term | Meaning |
|---|---|
| Epoch | One full pass through data |
| Batch | Small group of examples |
| Learning rate | How big steps to take |
| Dropout | Randomly turn off neurons |
| Loss | How wrong the model is |
| Backprop | How the model learns |

---

## Where To Practice

| Resource | Use |
|---|---|
| Google Colab | Free GPU |
| Kaggle | Free GPU + datasets |
| fast.ai | Best free course |
| PyTorch tutorials | Official docs |

---

## ✅ Done When

- [ ] You built an MLP
- [ ] You built a CNN
- [ ] You trained on GPU (Colab)
- [ ] You used transfer learning
