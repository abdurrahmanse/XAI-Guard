from typing import Any, Generic, Optional, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")

class StandardResponse(BaseModel, Generic[T]):
    success: bool = True
    data: T | None = None
    error: str | None = None
    meta: dict[str, Any] = Field(default_factory=dict)

def success_response(data: T, **meta) -> StandardResponse[T]:
    return StandardResponse(success=True, data=data, meta=meta)

def error_response(message: str, **meta) -> StandardResponse[Any]:
    return StandardResponse(success=False, error=message, meta=meta)
