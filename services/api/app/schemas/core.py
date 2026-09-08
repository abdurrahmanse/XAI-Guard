from datetime import datetime
from typing import Any, Literal, Optional

from pydantic import UUID4, BaseModel, Configdict, Field, IPvAnyAddress


class BaseSchema(BaseModel):
    model_config = Configdict(from_attributes=True, populate_by_name=True)

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
    tcp_flags: dict[str, bool] = Field(default_factory=dict)
    service: str = Field(max_length=64)
    features: dict[str, float]
    dataset_source: Literal["NSL_KDD", "CICIDS_2017", "UNSW_NB15", "BETH", "LIVE"]

class PredictionResponseSchema(BaseSchema):
    id: UUID4
    event_id: UUID4
    predicted_class: str
    confidence_score: float = Field(ge=0.0, le=1.0)
    class_probabilities: dict[str, float]
    severity_level: Literal["LOW", "MEDIUM", "HIGH", "CRITICAL"]
    inference_latency_ms: float
    is_shadow: bool
    explanation_task_id: str | None = None
    created_at: datetime

class FeatureVectorSchema(BaseSchema):
    features: list[float] = Field(min_length=1, max_length=1024)
    feature_names: list[str]
    vector_hash: str
