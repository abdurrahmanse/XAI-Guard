from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def health_check():
    """
    Check the health of the API and its dependent services.
    TODO: Add actual Redis and PostgreSQL ping.
    """
    return {
        "status": "ok",
        "service": "xai-guard-api",
        "stores": {"db": "pending", "cache": "pending", "artifacts": "pending"},
    }
