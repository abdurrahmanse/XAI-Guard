import enum
import uuid

from sqlalchemy import Boolean, Float, ForeignKey, Integer, String
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.dialects.postgresql import ARRAY, JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base, PrimaryKeyMixin, TimestampMixin


class ModelFrameworkEnum(str, enum.Enum):
    SKLEARN = "SKLEARN"
    XGBOOST = "XGBOOST"
    PYTORCH = "PYTORCH"

class ModelStatusEnum(str, enum.Enum):
    TRAINING = "TRAINING"
    REGISTERED = "REGISTERED"
    CHALLENGER = "CHALLENGER"
    CHAMPION = "CHAMPION"
    ARCHIVED = "ARCHIVED"

class ModelVersion(Base, PrimaryKeyMixin, TimestampMixin):
    __tablename__ = "model_versions"

    mlflow_run_id: Mapped[str] = mapped_column(String, unique=True, index=True)
    mlflow_model_name: Mapped[str] = mapped_column(String)
    mlflow_model_version: Mapped[int] = mapped_column(Integer)
    
    framework: Mapped[ModelFrameworkEnum] = mapped_column(SQLEnum(ModelFrameworkEnum))
    model_family: Mapped[str] = mapped_column(String)
    
    hyperparameters: Mapped[dict] = mapped_column(JSONB)
    metrics: Mapped[dict] = mapped_column(JSONB)
    feature_list: Mapped[list[str]] = mapped_column(ARRAY(String))
    
    dataset_version: Mapped[str] = mapped_column(String)
    git_sha: Mapped[str] = mapped_column(String(40))
    status: Mapped[ModelStatusEnum] = mapped_column(SQLEnum(ModelStatusEnum))
    is_shadow_active: Mapped[bool] = mapped_column(Boolean, default=False)

class PromotionHistory(Base, PrimaryKeyMixin, TimestampMixin):
    __tablename__ = "promotion_history"

    model_version_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("model_versions.id"))
    promoted_by: Mapped[str] = mapped_column(String)
    promotion_reason: Mapped[str] = mapped_column(String)
    f1_score_at_promotion: Mapped[float] = mapped_column(Float)
    latency_at_promotion: Mapped[float] = mapped_column(Float)
