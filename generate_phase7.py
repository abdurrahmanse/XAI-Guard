import os
import json

os.makedirs('services/api/app/schemas', exist_ok=True)
os.makedirs('services/api/app/core', exist_ok=True)
os.makedirs('packages/api-types/src', exist_ok=True)

# 7.1 Pydantic Core Schemas
with open('services/api/app/schemas/core.py', 'w') as f:
    f.write("""from pydantic import BaseModel, ConfigDict, Field, IPvAnyAddress, UUID4
from typing import Literal, Dict, Any, List, Optional
from datetime import datetime

class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

class SecurityEventInputSchema(BaseSchema):
    source_ip: IPvAnyAddress
    destination_ip: IPvAnyAddress
    source_port: int = Field(ge=0, le=65535)
    destination_port: int = Field(ge=0, le=65535)
    protocol: Literal["TCP", "UDP", "ICMP", "OTHER"]
    timestamp: datetime
    duration_ms: float = Field(ge=0.0)
    bytes_sent: int = Field(ge=0)
    bytes_received: int = Field(ge=0)
    packet_count: int = Field(ge=0)
    tcp_flags: Dict[str, bool] = Field(default_factory=dict)
    service: str = Field(max_length=64)
    features: Dict[str, float]
    dataset_source: Literal["NSL_KDD", "CICIDS_2017", "UNSW_NB15", "BETH", "LIVE"]

class PredictionResponseSchema(BaseSchema):
    id: UUID4
    event_id: UUID4
    predicted_class: str
    confidence_score: float = Field(ge=0.0, le=1.0)
    class_probabilities: Dict[str, float]
    severity_level: Literal["LOW", "MEDIUM", "HIGH", "CRITICAL"]
    inference_latency_ms: float
    is_shadow: bool
    explanation_task_id: Optional[str] = None
    created_at: datetime

class FeatureVectorSchema(BaseSchema):
    features: List[float] = Field(min_length=1, max_length=1024)
    feature_names: List[str]
    vector_hash: str
""")

# 7.2 Request/Response Normalization
with open('services/api/app/core/responses.py', 'w') as f:
    f.write("""from typing import Generic, TypeVar, Optional, Any
from pydantic import BaseModel, Field

T = TypeVar("T")

class StandardResponse(BaseModel, Generic[T]):
    success: bool = True
    data: Optional[T] = None
    error: Optional[str] = None
    meta: dict[str, Any] = Field(default_factory=dict)

def success_response(data: T, **meta) -> StandardResponse[T]:
    return StandardResponse(success=True, data=data, meta=meta)

def error_response(message: str, **meta) -> StandardResponse[Any]:
    return StandardResponse(success=False, error=message, meta=meta)
""")

# 7.3 Error Handling & Validation Exposing
with open('services/api/app/core/exceptions.py', 'w') as f:
    f.write("""from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from app.core.responses import error_response

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = []
    for error in exc.errors():
        field = ".".join(str(loc) for loc in error["loc"])
        errors.append(f"{field}: {error['msg']}")
    
    msg = "Validation Error: " + " | ".join(errors)
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=error_response(message=msg, validation_errors=exc.errors()).model_dump()
    )
""")

# 7.6 API Versioning & Deprecation
with open('services/api/app/core/versioning.py', 'w') as f:
    f.write("""from functools import wraps
from fastapi import Response
from datetime import datetime

def deprecated(sunset_date: str, alternative: str):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Extract response object if injected
            response: Response = kwargs.get('response')
            if response:
                response.headers["Deprecation"] = "true"
                response.headers["Sunset"] = sunset_date
                response.headers["Link"] = f'<{alternative}>; rel="alternate"'
            return await func(*args, **kwargs)
        return wrapper
    return decorator
""")

# 7.5 Zod Validation Strategy
with open('packages/api-types/package.json', 'w') as f:
    json.dump({
        "name": "@xaiguard/api-types",
        "version": "1.0.0",
        "main": "src/index.ts",
        "dependencies": {
            "zod": "^3.23.8"
        }
    }, f, indent=2)

with open('packages/api-types/src/index.ts', 'w') as f:
    f.write("""import { z } from "zod";

export const SecurityEventInputSchema = z.object({
  source_ip: z.string().ip(),
  destination_ip: z.string().ip(),
  source_port: z.number().int().min(0).max(65535),
  destination_port: z.number().int().min(0).max(65535),
  protocol: z.enum(["TCP", "UDP", "ICMP", "OTHER"]),
  timestamp: z.string().datetime(),
  duration_ms: z.number().min(0),
  bytes_sent: z.number().int().min(0),
  bytes_received: z.number().int().min(0),
  packet_count: z.number().int().min(0),
  tcp_flags: z.record(z.boolean()),
  service: z.string().max(64),
  features: z.record(z.number()),
  dataset_source: z.enum(["NSL_KDD", "CICIDS_2017", "UNSW_NB15", "BETH", "LIVE"]),
});

export const PredictionResponseSchema = z.object({
  id: z.string().uuid(),
  event_id: z.string().uuid(),
  predicted_class: z.string(),
  confidence_score: z.number().min(0).max(1),
  class_probabilities: z.record(z.number()),
  severity_level: z.enum(["LOW", "MEDIUM", "HIGH", "CRITICAL"]),
  inference_latency_ms: z.number(),
  is_shadow: z.boolean(),
  explanation_task_id: z.string().nullable().optional(),
  created_at: z.string().datetime(),
});

export class ApiValidationError extends Error {
  constructor(public zodError: z.ZodError) {
    super("API Response Validation Failed");
    this.name = "ApiValidationError";
  }
}

export function validateApiResponse<T>(schema: z.ZodSchema<T>, data: unknown): T {
  const result = schema.safeParse(data);
  if (!result.success) {
    throw new ApiValidationError(result.error);
  }
  return result.data;
}

export async function zodFetcher<T>(url: string, schema: z.ZodSchema<T>, init?: RequestInit): Promise<T> {
  const response = await fetch(url, init);
  if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
  const data = await response.json();
  return validateApiResponse(schema, data);
}

export type SecurityEventInput = z.infer<typeof SecurityEventInputSchema>;
export type PredictionResponse = z.infer<typeof PredictionResponseSchema>;
""")

print("Successfully generated Phase 7: API Schema Strategy.")
