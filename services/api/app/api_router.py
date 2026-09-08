from fastapi import APIRouter

from app.modules.admin.router import router as admin_router
from app.modules.alerts.router import router as alerts_router
from app.modules.auth.router import router as auth_router
from app.modules.events.router import router as events_router
from app.modules.explanations.router import router as explanations_router
from app.modules.health.router import router as health_router
from app.modules.inference.router import router as inference_router
from app.modules.registry.router import router as registry_router
from app.modules.training.router import router as training_router

# Core API Gateway
api_router = APIRouter()
api_router.include_router(health_router)
api_router.include_router(inference_router)
api_router.include_router(alerts_router)
api_router.include_router(registry_router)
api_router.include_router(events_router)
api_router.include_router(explanations_router)
api_router.include_router(training_router)
api_router.include_router(auth_router)
api_router.include_router(admin_router)
