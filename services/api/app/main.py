import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

from app.core.config import settings
from app.modules.alerts.router import router as alerts_router

# Module Routers
from app.modules.events.router import router as events_router
from app.modules.inference.router import router as inference_router
from app.modules.registry.router import router as registry_router
from app.modules.training.router import router as training_router

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
    app.include_router(training_router, prefix=f"{settings.API_V1_STR}/training", tags=["training"])

    @app.get("/v1/health", tags=["core"])
    async def health_check():
        return {"status": "healthy", "version": "1.0.0"}

    return app

app = create_application()
