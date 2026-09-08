import enum
import uuid

from sqlalchemy import Boolean, Float, ForeignKey, Index, String
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base, PrimaryKeyMixin, TimestampMixin


class SeverityEnum(str, enum.Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

class XAIMethodEnum(str, enum.Enum):
    SHAP = "SHAP"
    LIME = "LIME"
    ATTENTION = "ATTENTION"

class XAIStatusEnum(str, enum.Enum):
    PENDING = "PENDING"
    COMPUTING = "COMPUTING"
    COMPLETE = "COMPLETE"
    FAILED = "FAILED"

class Prediction(Base, PrimaryKeyMixin, TimestampMixin):
    __tablename__ = "predictions"

    event_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("security_events.id"), index=True)
    model_version_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("model_versions.id"), index=True)
    
    predicted_class: Mapped[str] = mapped_column(String)
    confidence_score: Mapped[float] = mapped_column(Float)
    class_probabilities: Mapped[dict] = mapped_column(JSONB)
    severity_level: Mapped[SeverityEnum] = mapped_column(SQLEnum(SeverityEnum))
    
    inference_latency_ms: Mapped[float] = mapped_column(Float)
    is_shadow: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
    
class XAIExplanation(Base, PrimaryKeyMixin, TimestampMixin):
    __tablename__ = "xai_explanations"

    prediction_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("predictions.id"), index=True)
    celery_task_id: Mapped[str] = mapped_column(String, index=True)
    
    method: Mapped[XAIMethodEnum] = mapped_column(SQLEnum(XAIMethodEnum))
    status: Mapped[XAIStatusEnum] = mapped_column(SQLEnum(XAIStatusEnum))
    feature_contributions: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
