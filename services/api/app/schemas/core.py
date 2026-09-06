from pydantic import BaseModel, ConfigDict, Field, IPvAnyAddress, UUID4
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
