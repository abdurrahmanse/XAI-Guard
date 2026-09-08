from fastapi import APIRouter

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/audit-logs")
async def get_audit_logs():
    """Mock audit logs endpoint."""
    return {"logs": []}


@router.get("/system-health")
async def get_system_health():
    """Mock system health endpoint."""
    return {"status": "healthy", "redis": "up", "postgres": "up"}
