import uuid

from sqlalchemy import Boolean, Float, ForeignKey, Index, Integer, String
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.dialects.postgresql import INET
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base, PrimaryKeyMixin, TimestampMixin
from app.modules.inference.models import SeverityEnum


class Alert(Base, PrimaryKeyMixin, TimestampMixin):
    __tablename__ = "alerts"

    prediction_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("predictions.id"), unique=True)
    severity: Mapped[SeverityEnum] = mapped_column(SQLEnum(SeverityEnum), index=True)
    attack_type: Mapped[str] = mapped_column(String, index=True)
    
    source_ip: Mapped[str] = mapped_column(INET, index=True)
    destination_ip: Mapped[str] = mapped_column(INET)
    confidence_score: Mapped[float] = mapped_column(Float)
    
    dedup_key: Mapped[str] = mapped_column(String, index=True)
    alert_count: Mapped[int] = mapped_column(Integer, default=1)
    
    acknowledged: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
