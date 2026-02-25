from uuid import UUID
from sqlalchemy import select

from app.database import async_session_maker
from app.operations.models import Operation


# Создание операции
async def create_operation(operation: Operation) -> Operation:
    async with async_session_maker() as session:
        session.add(operation)
        await session.commit()
        await session.refresh(operation)
        return operation
    

# Список операций
async def list_operations(client_id: UUID | None = None) -> list[Operation]:
    async with async_session_maker() as session:
        stmt = select(Operation).order_by(Operation.created_at.desc())

        if client_id:
            stmt = stmt.where(Operation.client_id == client_id)

        result = await session.execute(stmt)
        return result.scalars().all()