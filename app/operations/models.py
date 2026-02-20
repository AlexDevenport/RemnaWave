import enum
from datetime import datetime
import uuid
from sqlalchemy import ForeignKey, JSON, Text, Enum
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class OperationResult(str, enum.Enum):
    success = "success"
    fail = "fail"


class Operation(Base):
    __tablename__ = "operations"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    client_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("clients.id"))
    action: Mapped[str]
    payload: Mapped[dict] = mapped_column(JSON)
    result: Mapped[OperationResult] = mapped_column(Enum(OperationResult))
    error: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
