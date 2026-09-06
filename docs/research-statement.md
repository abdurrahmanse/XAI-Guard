# XAI-Guard Research Statement

## 1. Motivation
Modern cybersecurity operations centres (SOCs) are overwhelmed by alert fatigue. While Deep Learning models can detect zero-day attacks with high accuracy, their "black-box" nature prevents analysts from trusting them. Classical machine learning models are interpretable but often fail to capture complex, temporally distributed attack vectors. XAI-Guard seeks to bridge this gap by systematically evaluating the trade-offs between prediction performance, explainability, and operational fitness.

## 2. Problem Statement
**Central Research Question:** *Which AI model offers the best balance of accuracy, recall, false-positive control, explainability, inference latency, computational cost, and human usefulness for real-world cybersecurity threat detection?*

Currently, no consensus exists on whether the accuracy gains of Transformer-based architectures justify their high inference latency and computational cost in real-time Intrusion Detection Systems (IDS), nor which eXplainable AI (XAI) method provides the most actionable context for human analysts.

## 3. Research Objectives
1. Systematically compare classical ML, recurrent networks, and attention mechanisms on modern IDS benchmarks.
2. Quantify the stability and analyst-utility of three distinct XAI methods: SHAP, LIME, and Attention Rollout.
3. Establish a reproducible operational fitness metric that penalises models for high inference latency and memory bloat.

## 4. Scope
- **Six Competing Models:** Logistic Regression, Random Forest, XGBoost, LSTM, Transformer Encoder, Lightweight Transformer.
- **Four Benchmark Datasets:** NSL-KDD, CICIDS-2017, UNSW-NB15, BETH.
- **Three Evaluation Pillars:** Prediction Performance, Explainability Quality, Operational Fitness.

## 5. Expected Contributions
- A rigorous, open-source benchmarking framework for IDS models.
- A novel Composite Deployment Score (CDS) that balances F1, P99 Latency, and Memory usage.
- Empirical evidence on the correlation between XAI stability and prediction confidence.
