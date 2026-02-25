import uuid
from datetime import datetime
from enum import StrEnum, auto

from sqlalchemy import Enum, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column, Mapped

from app.database import Base


class ClientStatus(StrEnum):
    active = auto()
    blocked = auto()


class Client(Base):
    __tablename__ = "clients"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    status: Mapped[ClientStatus] = mapped_column(Enum(ClientStatus, name="clientstatus"), default=ClientStatus.active)
    expires_at: Mapped[datetime] = mapped_column(DateTime)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True,onupdate=datetime.utcnow)