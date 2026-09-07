# XAI-Guard: A Comparative Framework for Explainable Multi-Model Cybersecurity Threat Detection

## 1. Motivation
The proliferation of interconnected digital infrastructure has precipitated an exponential increase in the volume, velocity, and sophistication of cyberattacks. Modern Security Operations Centres (SOCs) rely heavily on Intrusion Detection Systems (IDS) to identify anomalous and malicious network behavior. However, the current operational paradigm is severely constrained by "alert fatigue"—a phenomenon where analysts are inundated with high volumes of low-fidelity alerts, leading to cognitive overload and critical threat latency. 

While Deep Learning (DL) architectures have demonstrated state-of-the-art predictive performance in identifying zero-day vulnerabilities and complex attack signatures, their inherently opaque, "black-box" nature fundamentally undermines human trust. Conversely, classical machine learning models (e.g., Logistic Regression, Decision Trees) offer high interpretability but frequently fail to capture the nonlinear, temporally distributed attack vectors characteristic of modern Advanced Persistent Threats (APTs). To operationalize AI in high-stakes cybersecurity environments, the industry urgently requires a paradigm shift from purely performance-optimised models to systems that intrinsically balance predictive accuracy with human-interpretable explanations and computational efficiency.

## 2. Problem Statement
The central research question driving the XAI-Guard project is: 

*Which Artificial Intelligence model architecture offers the most optimal, mathematically quantifiable balance of predictive accuracy, recall, false-positive control, algorithmic explainability, inference latency, computational training cost, and human-analyst usefulness for real-world cybersecurity threat detection?*

Currently, the cybersecurity research community lacks a standardized, multi-pillar evaluation framework to objectively benchmark these competing priorities. There is no empirical consensus on whether the marginal accuracy gains provided by complex, high-parameter architectures (such as Transformer Encoders) justify their substantial inference latency and GPU-hour training costs in real-time edge environments. Furthermore, while eXplainable AI (XAI) techniques exist, it remains undetermined which methodology provides the most actionable, stable, and causally sound context for a human SOC analyst investigating a live threat.

## 3. Research Objectives
To address this critical gap, the XAI-Guard research project establishes the following core objectives:
1. **Architectural Benchmarking:** Systematically evaluate and compare the efficacy of classical machine learning, tree-based ensembles, recurrent neural networks, and self-attention mechanisms across modern, heterogeneous IDS benchmarks.
2. **XAI Stability and Utility Quantification:** Empirically quantify the mathematical stability and practical analyst-utility of three distinct interpretability paradigms: Shapley Additive exPlanations (SHAP), Local Interpretable Model-agnostic Explanations (LIME), and Attention Rollout.
3. **Operational Viability Assessment:** Formulate and validate a reproducible, hardware-agnostic operational fitness metric that mathematically penalizes architectures for excessive inference latency, memory bloat, and carbon-intensive training cycles.
4. **Resilience to Concept Drift:** Measure the degradation rate of complex neural architectures versus classical models when exposed to temporal data drift and zero-day topological shifts in live honeypot environments.

## 4. Scope
The scope of this research is strictly bounded to ensure reproducibility and statistical significance.
- **Competing Model Families (6):** 
  1. Logistic Regression (Baseline)
  2. Random Forest
  3. Extreme Gradient Boosting (XGBoost)
  4. Long Short-Term Memory Networks (LSTM)
  5. Full Transformer Encoder
  6. Lightweight Transformer (Optimised for Edge/CPU inference)
- **Benchmark Datasets (4):** 
  1. *NSL-KDD* (Historical baseline)
  2. *CICIDS-2017* (Modern network flow analysis)
  3. *UNSW-NB15* (Comprehensive multi-class CVE taxonomy)
  4. *BETH* (Real-world enterprise honeypot exhibiting temporal drift)
- **Evaluation Pillars (3):** 
  1. *Prediction Performance* (F1-Macro, ROC-AUC, PR-AUC)
  2. *Explainability Quality* (SHAP Stability, LIME Rank Correlation, Analyst Utility)
  3. *Operational Fitness* (P99 Latency, Throughput, Memory footprint, GPU-hours)

## 5. Expected Contributions
The XAI-Guard project anticipates delivering the following seminal contributions to the fields of Applied Machine Learning and Cybersecurity:
- **The XAI-Guard Benchmarking Framework:** An open-source, extensible, and containerized platform for the reproducible evaluation of IDS models across competing datasets.
- **The Composite Deployment Score (CDS):** The introduction of a novel, weighted mathematical metric (`CDS = 0.40 × norm(F1) + 0.35 × norm(1/latency_p99) + 0.25 × norm(1/memory_mb)`) that provides a single, actionable heuristic for automated Champion/Challenger model promotion in MLOps pipelines.
- **Empirical XAI Findings:** Conclusive, peer-review-ready evidence regarding the correlation between predictive confidence, XAI feature stability, and the practical utility of explanations in reducing Mean Time To Respond (MTTR) for human analysts.
