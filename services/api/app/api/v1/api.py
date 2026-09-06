from fastapi import APIRouter

from .endpoints import alerts, health, inference, models

api_router = APIRouter()
api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(inference.router, tags=["inference"])
api_router.include_router(alerts.router, prefix="/alerts", tags=["alerts"])
api_router.include_router(models.router, prefix="/models", tags=["models"])
