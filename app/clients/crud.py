# Здесь будет осуществляться работа с БД
from datetime import datetime, timedelta
from uuid import UUID
from sqlalchemy import select

from app.database import async_session_maker
from app.clients.models import Client, ClientStatus


# Создание нового клиента
async def create_client() -> Client:
    client = Client(
        status=ClientStatus.active,
        expires_at=datetime.utcnow() + timedelta(days=30),
    )

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
        await session.delete(client)
        await session.commit()


# Продление времени клиента
async def extend_client(
    client: Client, 
    days: int
) -> None:
    async with async_session_maker() as session:

        db_client = await session.get(Client, client.id)

        if db_client.expires_at:
            db_client.expires_at += timedelta(days=days)
        else:
            db_client.expires_at = datetime.utcnow() + timedelta(days=days)

        await session.commit()
        await session.refresh(db_client)

        return db_client


# Блокировка клиента
async def block_client(client: Client) -> None:
    async with async_session_maker() as session:
        db_client = await session.get(Client, client.id)
        db_client.status = ClientStatus.blocked
        await session.commit()


# Разблокировка клиента
async def unblock_client(client: Client) -> None:
    async with async_session_maker() as session:
        db_client = await session.get(Client, client.id)
        db_client.status = ClientStatus.active
        await session.commit()