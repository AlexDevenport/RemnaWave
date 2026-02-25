from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime
from enum import Enum


# Результат операции
class SOperationResult(str, Enum):
    success = "success"
    fail = "fail"


# Ответ операции
class SOperationResponse(BaseModel):
    id: UUID
    client_id: UUID
    action: str
    payload: dict | None = None
    result: SOperationResult
    error: str | None = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)