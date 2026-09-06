# 02 — System Architecture

> **Phases 4 · 5** — System design, API contracts, and data schema definitions.

---

## Phase 4 — System Architecture Design

**Goal:** Produce the definitive system architecture document before any service code is written. All subsequent implementation phases reference this document.

**Context:** XAI-Guard has four distinct layers: Data Ingestion → ML Pipeline → API/Serving → Dashboard. The ML pipeline is the research core. The serving layer must support real-time inference (< 100 ms P99) and async explanation generation. Architecture must be horizontally scalable.

**Tools:** Mermaid (diagrams), OpenAPI 3.1 (contracts), draw.io (optional)

**Tasks:**

- [ ] 4.1 Draw the end-to-end data flow diagram (`docs/architecture-diagram.md`):

```
Security Events
      │
      ▼
 Data Ingestion (POST /v1/events)
      │
      ▼
 Feature Pipeline (ml/src/features/)
      │
      ├──────────┬──────────┐
      ▼          ▼          ▼
  XGBoost      LSTM    Transformer
      │          │          │
      └──────────┴──────────┘
                 │
          Model Evaluation
                 │
      ┌──────────┼──────────┐
      ▼          ▼          ▼
 Performance   XAI       Cost
                 │
          Model Registry
           (Champion/Challenger)
                 │
          Production Model
                 │
          Security Dashboard
```

- [ ] 4.2 Define component boundaries and inter-service contracts:
  - `apps/web` → `services/api` (REST + WebSocket)
  - `services/api` → `ml/src/` (in-process, model loaded into memory)
  - `services/api` → PostgreSQL (SQLAlchemy async)
  - `services/api` → Redis (prediction cache, Celery queue)
  - `services/api` → MinIO (model artifact loading via MLflow)
- [ ] 4.3 Design Model Registry schema (DB table `model_registry`):
  - `champion_model_id` — currently serving all live traffic
  - `challenger_model_id` — running in shadow mode
  - `promotion_criteria` JSONB — `{f1_delta: 0.02, auc_delta: 0.01, latency_budget_ms: 100}`
  - `last_evaluation_at`, `status`
- [ ] 4.4 Define Inference Service API surface:
  - `POST /v1/predict` — primary inference endpoint
  - `POST /v1/explain` — async explanation request
  - `GET /v1/explain/{task_id}` — poll explanation result
  - `GET /v1/models` — model registry overview
  - `GET /v1/alerts` — paginated alert feed
  - `GET /v1/ws/alerts` — WebSocket real-time alert stream
  - `GET /v1/health` — service health check
- [ ] 4.5 Define the Champion/Challenger evaluation loop:
  - Challenger receives all events in shadow mode (async, does not affect response time)
  - Nightly Celery job compares Champion vs Challenger on last 24h shadow predictions
  - If Challenger exceeds thresholds → auto-promote; old Champion → archived
  - `POST /v1/models/rollback` reverts to previous Champion
- [ ] 4.6 Define the canonical security event schema:
  ```json
  {
    "timestamp": "ISO8601",
    "source_ip": "IPv4/IPv6",
    "dest_ip": "IPv4/IPv6",
    "source_port": 0-65535,
    "dest_port": 0-65535,
    "protocol": "TCP|UDP|ICMP",
    "payload_size_bytes": integer,
    "duration_ms": integer,
    "flags": ["SYN", "ACK", ...],
    "dataset_source": "cicids2017|nsl-kdd|unsw-nb15|live"
  }
  ```
- [ ] 4.7 Document latency budget (all P99 targets):
  - Ingestion & validation: < 5 ms
  - Feature extraction: < 10 ms
  - Model inference (Champion): < 50 ms
  - DB write (async): < 20 ms
  - Total prediction P99: **< 100 ms**
  - SHAP explanation: < 500 ms (async Celery task)
  - Dashboard first render: < 2 s
  - Alert WebSocket delivery: < 10 s from event
- [ ] 4.8 Identify external integrations: AbuseIPDB (IP reputation), MITRE ATT&CK (attack taxonomy), SIEM webhook receivers (Splunk/Elastic format)

**Output:** `docs/architecture-diagram.md`, `docs/api-contracts.md`, `docs/latency-budget.md`

---

## Phase 5 — API Contract & Data Schema Definitions

**Goal:** Lock down all API contracts and shared data schemas before implementation — API-first development prevents integration failures between teams.

**Context:** ML, backend, and frontend teams work in parallel. Shared schemas are the contract. Pydantic v2 is used in Python (FastAPI auto-generates OpenAPI). Zod is used in TypeScript (Next.js). Contract tests enforce parity.

**Tools:** FastAPI (OpenAPI generation), Pydantic v2, Zod, TypeScript

**Tasks:**

- [ ] 5.1 Write `services/api/schemas/event.py`:
  ```python
  class SecurityEvent(BaseModel):
      timestamp: datetime
      source_ip: IPvAnyAddress
      dest_ip: IPvAnyAddress
      source_port: int = Field(ge=0, le=65535)
      dest_port: int = Field(ge=0, le=65535)
      protocol: Literal["TCP", "UDP", "ICMP"]
      payload_size_bytes: int = Field(ge=0)
      duration_ms: int = Field(ge=0)
      flags: list[str] = []
      dataset_source: str = "live"

  class PredictionResponse(BaseModel):
      prediction_id: UUID
      attack_type: AttackType  # enum
      confidence: float = Field(ge=0.0, le=1.0)
      severity: SeverityLevel  # enum: critical/high/medium/low
      model_version: str
      latency_ms: float
      explanation_task_id: UUID | None = None
  ```
- [ ] 5.2 Write `services/api/schemas/explanation.py` — `SHAPExplanation`, `LIMEExplanation`, `AttentionExplanation` Pydantic models with `feature_contributions: list[{name, value, direction}]`
- [ ] 5.3 Write `services/api/schemas/model.py` — `ModelMetadata`, `EvaluationResult`, `ChampionChallengerStatus` schemas
- [ ] 5.4 Generate OpenAPI spec: `uvicorn services.api.main:app; curl localhost:8000/openapi.json > docs/openapi.yaml`
- [ ] 5.5 Write TypeScript Zod schemas in `packages/ui/src/types/` — mirror every Pydantic model exactly
- [ ] 5.6 Write contract tests: `tests/contracts/test_schema_parity.py` — parse TypeScript Zod types, compare field names and types against Pydantic schemas
- [ ] 5.7 Define all enums as shared constants:
  - `AttackType`: `ddos`, `port_scan`, `brute_force`, `botnet`, `web_attack`, `infiltration`, `normal`
  - `SeverityLevel`: `critical` (≥0.90), `high` (0.75–0.90), `medium` (0.50–0.75), `low` (<0.50)
  - `ModelStatus`: `champion`, `challenger`, `archived`, `training`
  - `ExplanationType`: `shap`, `lime`, `attention`

**Output:** Complete OpenAPI spec at `docs/openapi.yaml`, Pydantic schemas in `services/api/schemas/`, Zod schemas in `packages/ui/src/types/`, contract tests passing

---

## Phase Map

| Phase | Title | Key Output |
|-------|-------|------------|
| P4 | System Architecture | Architecture diagram, latency budget, component boundaries |
| P5 | API Contracts | OpenAPI spec, Pydantic schemas, Zod schemas, contract tests |

**Previous:** ← [01 — Project Foundation](01-project-foundation.md) | **Next:** → [03 — Data Engineering](03-data-engineering.md)