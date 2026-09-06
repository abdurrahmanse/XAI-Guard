import os

# 6.1 Module Catalogue
with open('docs/module-catalogue.md', 'w') as f:
    f.write("""# XAI-Guard Module Catalogue & Boundary Rules

To prevent our FastAPI backend from degrading into a Big Ball of Mud, we enforce strict domain boundaries. Modules may only communicate via public interfaces (`service.py`) and must never import another module's SQLAlchemy models directly.

## Module Boundaries

| Module | Ownership Scope | Public Interface | Celery Tasks | Forbidden Imports |
|--------|----------------|------------------|--------------|-------------------|
| `core` | DB engine, Config, Logging, Exception Handlers | `get_db()`, `settings` | None | ALL other modules |
| `auth` | Users, JWTs, RBAC, Audit Logs | `verify_token()`, `log_audit()` | None | `events`, `predictions` |
| `events` | Security Events, deduplication hash | `ingest_event()` | `process_event` | `predictions`, `models` |
| `predictions` | ML Inference, confidence thresholds | `predict()` | `batch_predict` | `auth`, `alerts` |
| `explanations`| SHAP/LIME computation | `generate_xai()` | `compute_shap` | `auth`, `events` |
| `registry` | Model versions, Champion/Challenger status | `get_champion()`, `promote()` | `nightly_eval` | `alerts`, `auth` |
| `alerts` | Severity routing, WebSocket broadcasting | `trigger_alert()` | None | `models`, `explanations`|
| `drift` | MMD Drift Reports | `calculate_drift()` | `drift_monitor`| `auth`, `alerts` |
| `threat_intel`| AbuseIPDB, MITRE taxonomy | `enrich_ip()` | `refresh_tor`| `events`, `models` |

## Architecture

```mermaid
graph TD
    API[FastAPI Router] -->|POST /events| Events[Events Module]
    Events -->|publishes| Celery[Celery Queue]
    Celery --> Predictions[Predictions Module]
    Predictions -->|if anomaly| Alerts[Alerts Module]
    Predictions -->|async trigger| Explanations[Explanations Module]
    Alerts --> WS[WebSocket Dashboard]
    
    subgraph Data Layer
        Predictions --> DB[(PostgreSQL)]
        Models[Registry Module] --> DB
        Events --> DB
    end
```
""")

# 6.2 Application Factory
with open('services/api/app/main.py', 'w') as f:
    f.write("""from fastapi import FastAPI
from contextlib import asynccontextmanager
from prometheus_fastapi_instrumentator import Instrumentator
import logging

from app.core.config import settings

# Module Routers
from app.modules.events.router import router as events_router
from app.modules.inference.router import router as inference_router
from app.modules.registry.router import router as registry_router
from app.modules.alerts.router import router as alerts_router

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up XAI-Guard API...")
    # Initialize DB engines, warm caches, load Champion model here
    yield
    logger.info("Shutting down XAI-Guard API...")
    # Cleanup DB engines and Celery queues here

def create_application() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version="1.0.0",
        openapi_url="/openapi.json",
        lifespan=lifespan
    )

    # Middleware
    # (CORS, Security headers would be added here)

    # Prometheus Instrumentation
    Instrumentator().instrument(app).expose(app)

    # Register Module Routers
    app.include_router(events_router, prefix=f"{settings.API_V1_STR}/events", tags=["events"])
    app.include_router(inference_router, prefix=f"{settings.API_V1_STR}/inference", tags=["inference"])
    app.include_router(registry_router, prefix=f"{settings.API_V1_STR}/registry", tags=["registry"])
    app.include_router(alerts_router, prefix=f"{settings.API_V1_STR}/alerts", tags=["alerts"])

    @app.get("/v1/health", tags=["core"])
    async def health_check():
        return {"status": "healthy", "version": "1.0.0"}

    return app

app = create_application()
""")

# 6.3 Celery App Configuration
os.makedirs('services/api/app/core/celery', exist_ok=True)
with open('services/api/app/core/celery_app.py', 'w') as f:
    f.write("""from celery import Celery
from app.core.config import settings

celery_app = Celery(
    "xaiguard",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
)

celery_app.conf.update(
    task_serializer="json", # msgspec can be configured here natively if wrapped
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    
    # Queue Routing
    task_routes={
        'app.modules.events.tasks.*': {'queue': 'events'},
        'app.modules.explanations.tasks.*': {'queue': 'explanations'},
        'app.modules.drift.tasks.*': {'queue': 'pipeline'},
        'app.modules.registry.tasks.*': {'queue': 'pipeline'},
    },
    
    # Task scheduling (Beat)
    beat_schedule={
        'nightly-champion-evaluation': {
            'task': 'app.modules.registry.tasks.nightly_eval',
            'schedule': 86400.0, # Every 24 hours
        },
    }
)
""")

# 6.4 OpenAPI Types Script
os.makedirs('packages/api-types', exist_ok=True)
with open('services/api/scripts/generate-types.sh', 'w') as f:
    f.write("""#!/bin/bash
# Generate TypeScript types from FastAPI OpenAPI spec

echo "Downloading OpenAPI Spec..."
# Wait for API to boot in CI
sleep 5

curl -s http://localhost:8000/openapi.json > /tmp/openapi.json

echo "Generating TypeScript interfaces..."
pnpm dlx openapi-typescript /tmp/openapi.json -o ../../packages/api-types/index.ts

echo "Types successfully generated in packages/api-types/index.ts"
""")
os.chmod('services/api/scripts/generate-types.sh', 0o755)

print("Successfully generated Phase 6: Modular Monolith Architecture implementations.")
