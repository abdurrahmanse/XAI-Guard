from fastapi import APIRouter

from app.modules.alerts.router import router as alerts_router
from app.modules.health.router import router as health_router
from app.modules.inference.router import router as inference_router
from app.modules.registry.router import router as registry_router

api_router = APIRouter()
api_router.include_router(health_router)
api_router.include_router(inference_router)
api_router.include_router(alerts_router)
api_router.include_router(registry_router)
