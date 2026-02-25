from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime
from enum import Enum


# Статус ответа
class SClientStatus(str, Enum):
    active = "active"
    blocked = "blocked"


# Ответ для клиента
class SClientResponse(BaseModel):
    id: UUID
    status: SClientStatus
    expires_at: datetime
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# Ответ при создании
class SClientCreate(BaseModel):
    id: UUID


# Extend
class SClientExtend(BaseModel):
    days: int