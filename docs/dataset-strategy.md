# Dataset Strategy & Attack Taxonomy

## 1. NSL-KDD
- **Context:** The established historical benchmark for IDS.
- **Profile:** 40 features, balanced classes.
- **Challenge:** Solved dataset, used primarily for baseline verification.

## 2. CICIDS-2017
- **Context:** Modern network flows with realistic background traffic.
- **Profile:** 80 features, severe class imbalance (Normal traffic dominates).
- **Challenge:** Detecting low-frequency attacks like Infiltration and WebAttacks.

## 3. UNSW-NB15
- **Context:** Comprehensive attack taxonomy representing modern CVEs.
- **Profile:** 49 features, 9 detailed attack families.
- **Challenge:** Multi-class classification complexity.

## 4. BETH
- **Context:** Real enterprise-scale honeypot data with heavy temporal drift.
- **Challenge:** Evaluating model robustness to concept drift over time.

## Unified Attack Taxonomy
To train a single unified platform, all dataset-specific labels are mapped to the following standard `Enum`:
1. `DDOS`
2. `PORT_SCAN`
3. `BRUTE_FORCE`
4. `BOTNET`
5. `WEB_ATTACK`
6. `INFILTRATION`
7. `NORMAL`

*(Attack subtypes with fewer than 100 samples are flagged for SMOTE/ADASYN augmentation).*
