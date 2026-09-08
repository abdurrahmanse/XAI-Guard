import uuid

from app.core.database import Base, PrimaryKeyMixin, TimestampMixin
from app.modules.events.models import DatasetSourceEnum
from sqlalchemy import Boolean, Float, ForeignKey, Index
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column


class DriftReport(Base, PrimaryKeyMixin, TimestampMixin):
    __tablename__ = "drift_reports"

    model_version_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("model_versions.id"), index=True)
    dataset_source: Mapped[DatasetSourceEnum] = mapped_column(SQLEnum(DatasetSourceEnum, name="datasetsourceenum", create_type=False))
    
    drift_score_mmd: Mapped[float] = mapped_column(Float)
    is_drift_detected: Mapped[bool] = mapped_column(Boolean, default=False)
    features_drifted: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
