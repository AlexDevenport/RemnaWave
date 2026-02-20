# Здесь будет осуществляться работа с БД
from datetime import datetime, timedelta
from uuid import UUID
from sqlalchemy import select

from app.database import async_session_maker
from app.clients.models import Client, ClientStatus


# Создание нового клиента
async def create_client() -> Client:
    client = Client(expires_at=datetime.utcnow())

    async with async_session_maker() as session:
        session.add(client)
        await session.commit()
        await session.refresh(client)

    return client


# Получение списка всех клиентов
async def list_clients() -> list[Client]:
    async with async_session_maker() as session:
        result = await session.execute(select(Client))

        return result.scalars().all()


# Получение клиента по id
async def get_client(client_id: UUID) -> Client | None:
    async with async_session_maker() as session:

        return await session.get(Client, client_id)


# Удаление клиента
async def delete_client(client: Client) -> None:
    async with async_session_maker() as session:
        client.status = ClientStatus.blocked
        await session.merge(client)
        await session.commit()


# Продление времени клиента
async def extend_client(
    client: Client, 
    days: int
) -> Client:
    async with async_session_maker() as session:
        if client.expires_at:
            client.expires_at += timedelta(days=days)
        else:
            client.expires_at = datetime.utcnow() + timedelta(days=days)
        
        await session.merge(client)
        await session.commit()
        await session.refresh(client)

    return client


# Блокировка клиента
async def block_client(client: Client) -> None:
    async with async_session_maker() as session:
        client.status = ClientStatus.blocked
        await session.merge(client)
        await session.commit()


# Разблокировка клиента
async def unblock_client(client: Client) -> None:
    async with async_session_maker() as session:
        client.status = ClientStatus.active
        await session.merge(client)
        await session.commit()