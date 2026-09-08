import datetime
import enum
import uuid

from sqlalchemy import Boolean, DateTime, ForeignKey, Index, String
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.dialects.postgresql import INET, JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base, PrimaryKeyMixin, TimestampMixin


class UserRoleEnum(str, enum.Enum):
    ANALYST = "ANALYST"
    ADMIN = "ADMIN"

class AuditActionEnum(str, enum.Enum):
    LOGIN = "LOGIN"
    LOGOUT = "LOGOUT"
    PROMOTE_MODEL = "PROMOTE_MODEL"
    ROLLBACK_MODEL = "ROLLBACK_MODEL"
    ACKNOWLEDGE_ALERT = "ACKNOWLEDGE_ALERT"
    EXPORT_REPORT = "EXPORT_REPORT"
    UPDATE_TAXONOMY = "UPDATE_TAXONOMY"

class User(Base, PrimaryKeyMixin, TimestampMixin):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(String, unique=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String)
    
    role: Mapped[UserRoleEnum] = mapped_column(SQLEnum(UserRoleEnum))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    last_login_at: Mapped[datetime.datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

class AuditLog(Base, PrimaryKeyMixin, TimestampMixin):
    __tablename__ = "audit_logs"

    user_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("users.id"), nullable=True, index=True)
    action: Mapped[AuditActionEnum] = mapped_column(SQLEnum(AuditActionEnum))
    
    resource_type: Mapped[str] = mapped_column(String)
    resource_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("model_versions.id"), nullable=True) # Loosely coupled for other resources too, but UUID typed.
    
    ip_address: Mapped[str | None] = mapped_column(INET, nullable=True)
    user_agent: Mapped[str | None] = mapped_column(String, nullable=True)
    details: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
