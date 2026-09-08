import enum

from sqlalchemy import BigInteger, Float, Index, Integer, String
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.dialects.postgresql import INET, JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base, PrimaryKeyMixin, TimestampMixin


class ProtocolEnum(str, enum.Enum):
    TCP = "TCP"
    UDP = "UDP"
    ICMP = "ICMP"
    OTHER = "OTHER"

class DatasetSourceEnum(str, enum.Enum):
    NSL_KDD = "NSL_KDD"
    CICIDS_2017 = "CICIDS_2017"
    UNSW_NB15 = "UNSW_NB15"
    BETH = "BETH"
    LIVE = "LIVE"

class SecurityEvent(Base, PrimaryKeyMixin, TimestampMixin):
    __tablename__ = "security_events"

    dedup_hash: Mapped[str] = mapped_column(String, unique=True, index=True)
    source_ip: Mapped[str] = mapped_column(INET, index=True)
    destination_ip: Mapped[str] = mapped_column(INET, index=True)
    source_port: Mapped[int] = mapped_column(Integer)
    destination_port: Mapped[int] = mapped_column(Integer)
    protocol: Mapped[ProtocolEnum] = mapped_column(SQLEnum(ProtocolEnum))
    timestamp: Mapped[str] = mapped_column(String, index=True) # Stored as ISO string or TIMESTAMPTZ
    
    duration_ms: Mapped[float] = mapped_column(Float)
    bytes_sent: Mapped[int] = mapped_column(BigInteger)
    bytes_received: Mapped[int] = mapped_column(BigInteger)
    packet_count: Mapped[int] = mapped_column(Integer)
    tcp_flags: Mapped[dict] = mapped_column(JSONB)
    service: Mapped[str] = mapped_column(String(64))
    
    features: Mapped[dict] = mapped_column(JSONB)
    dataset_source: Mapped[DatasetSourceEnum] = mapped_column(SQLEnum(DatasetSourceEnum))
    threat_intel_data: Mapped[dict | None] = mapped_column(JSONB, nullable=True)

    __table_args__ = (
        Index("ix_security_events_threat_intel_null", "threat_intel_data", postgresql_where=threat_intel_data.is_(None)),
    )
