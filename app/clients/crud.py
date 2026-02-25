# Здесь будет осуществляться работа с БД
from datetime import datetime, timedelta
from uuid import UUID
from sqlalchemy import select

from app.database import async_session_maker
from app.clients.models import Client, ClientStatus


# Создание нового клиента
async def create_client(days: int) -> Client:
    client = Client(
        status=ClientStatus.active,
        expires_at=datetime.utcnow() + timedelta(days=days)
    )

    async with async_session_maker() as session:
        session.add(client)
        await session.commit()
        await session.refresh(client)

    return client


# Получение списка всех клиентов
async def list_clients(
    status: ClientStatus | None = None,
    expired: bool | None = None
) -> list[Client]:
    async with async_session_maker() as session:
        stmt = select(Client).order_by(Client.created_at.desc())

    if status is not None:
        stmt = stmt.where(Client.status == status)

    if expired is not None:
        now = datetime.utcnow()
        
        if expired:
            stmt = stmt.where(Client.expires_at < now)
        else:
            stmt = stmt.where(Client.expires_at >= now)
    
    result = await session.execute(stmt)
    
    return result.scalars().all()


# Получение клиента по id
async def get_client(client_id: UUID) -> Client | None:
    async with async_session_maker() as session:

        return await session.get(Client, client_id)


# Удаление клиента
async def delete_client(client: Client) -> None:
    async with async_session_maker() as session:
        await session.delete(client)
        await session.commit()


# Продление времени клиента
async def extend_client(
    client_id: UUID, 
    days: int
) -> None:
    async with async_session_maker() as session:
        client = await session.get(Client, client_id)

        if not client:
            return None
        
        if client.expires_at:
            client.expires_at += timedelta(days=days)
        else:
            client.expires_at = datetime.utcnow() + timedelta(days=days)

        await session.commit()
        await session.refresh(client)
        
        return client


# Блокировка клиента
async def block_client(client_id: UUID) -> None:
    async with async_session_maker() as session:
        client = await session.get(Client, client_id)

        if not client:
            return None

        client.status = ClientStatus.blocked
        await session.commit()
        await session.refresh(client)

        return client


# Разблокировка клиента
async def unblock_client(client_id: UUID) -> None:
    async with async_session_maker() as session:
        client = await session.get(Client, client_id)

        if not client:
            return None

        client.status = ClientStatus.active
        await session.commit()
        await session.refresh(client)

        return client