| Model                   |   F1 Macro |   Latency P99 (ms) |   Memory (MB) |   CDS |
|:------------------------|-----------:|-------------------:|--------------:|------:|
| Transformer (Quantised) |      0.957 |                8.4 |           2.4 | 0.947 |
| XGBoost                 |      0.931 |                3.1 |          45.2 | 0.884 |
| BiLSTM                  |      0.941 |               14.5 |          18.5 | 0.742 |
| Logistic Regression     |      0.72  |                0.5 |           2.1 | 0.635 |
| Random Forest           |      0.902 |                4.2 |         120.5 | 0.612 |
| Transformer (Full)      |      0.965 |               28.3 |         155   | 0.4   |