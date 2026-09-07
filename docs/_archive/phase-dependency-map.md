# Phase Dependency Map

```mermaid
graph TD
    %% Layer 1: Foundation
    subgraph L1 [L1: Foundation P1-P8]
        P1[P1: Research Scoping] --> P2[P2: Charter & Scope]
        P2 --> P3[P3: Dev Environment]
        P3 --> P4[P4: Architecture]
        P4 --> P5[P5: API Contracts]
        P5 --> P6[P6: Modular Monolith]
        P6 --> P7[P7: API Schemas]
        P7 --> P8[P8: API Routing]
    end

    %% Layer 2: Data Engineering
    subgraph L2 [L2: Data P9-P17]
        P8 --> P9[P9: Ingestion Core]
        P9 --> P10[P10: DVC Setup]
        P10 --> P11[P11: Raw Data ETL]
        P11 --> P12[P12: Imputation]
        P12 --> P13[P13: Feature Scaling]
        P13 --> P14[P14: Time-Series Windows]
        P14 --> P15[P15: Class Imbalance]
        P15 --> P16[P16: PCA Reduction]
        P16 --> P17[P17: DVC Push]
    end

    %% Layer 3: ML Tracking
    subgraph L3 [L3: ML Tracking P18-P25]
        P17 --> P18[P18: MLflow Backend]
        P18 --> P20[P20: Dataset Registry]
        P20 --> P25[P25: CMI Implementation]
    end

    %% Layer 4: ML Research (Parallelizable)
    subgraph L4 [L4: ML Research P26-P39]
        P25 --> P26[P26: Logistic Regression]
        P25 --> P28[P28: Random Forest]
        P25 --> P30[P30: XGBoost]
        P25 --> P32[P32: LSTM]
        P25 --> P34[P34: Transformer]
        P25 --> P36[P36: Light Transformer]
        
        P26 --> P39[P39: Research Checkpoint]
        P28 --> P39
        P30 --> P39
        P32 --> P39
        P34 --> P39
        P36 --> P39
    end

    %% Layer 5: XAI & UI
    subgraph L5 [L5: XAI & Fullstack P40-P63]
        P39 --> P40[P40: SHAP Integration]
        P40 --> P44[P44: Celery Workers]
        P44 --> P50[P50: Champion Promotion]
        P50 --> P55[P55: Dashboard Frontend]
        P55 --> P60[P60: CI/CD Pipeline]
        P60 --> P63[P63: Project Wrap]
    end
```

**Critical Path:** P1 → P17 (Data) → P25 (Interface) → P34 (Transformer) → P39 (Checkpoint) → P44 (Celery) → P55 (Dashboard) → P63 (Finish).
**Parallelization:** Phases 26 through 38 (The six ML models) can be executed concurrently by separate research teams.
