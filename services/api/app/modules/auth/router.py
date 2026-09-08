from fastapi import APIRouter

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login")
async def login():
    """Mock login endpoint."""
    return {"access_token": "mock_token", "token_type": "bearer"}


@router.post("/register")
async def register():
    """Mock register endpoint."""
    return {"message": "User registered successfully."}


@router.get("/me")
async def get_current_user():
    """Mock get current user endpoint."""
    return {"id": "uuid", "username": "admin", "role": "ADMIN"}
