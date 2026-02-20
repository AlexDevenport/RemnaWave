from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from enum import Enum


class SClientStatus(str, Enum):
    active = "active"
    blocked = "blocked"


# Ответ для клиента
class SClientResponse(BaseModel):
    id: UUID
    status: SClientStatus
    expires_at: datetime
    created_at: datetime

    class Config:
        from_attributes = True


# Ответ при создании
class SClientCreate(BaseModel):
    id: UUID


# Extend
class SClientExtend(BaseModel):
    days: int