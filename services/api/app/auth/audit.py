from sqlalchemy import JSON, Column, Integer, String

from app.core.database import Base, PrimaryKeyMixin, TimestampMixin


class AuditLog(Base, PrimaryKeyMixin, TimestampMixin):
    __tablename__ = "audit_logs"
    action = Column(String)
