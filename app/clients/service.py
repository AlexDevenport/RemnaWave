from datetime import datetime
from fastapi import HTTPException, status
from uuid import UUID

from app.clients import crud
from app.clients.shemas import SClientResponse, SClientCreate


# Создание клиента
async def create_client() -> SClientCreate:
    client = await crud.create_client()
    return SClientCreate(id=client.id)


# Получение всех клиентов
async def list_clients(
    status=None,
    expired=None
) -> list[SClientResponse]:
    clients = await crud.list_clients()

    if status:
        clients = [c for c in clients if c.status == status]

    if expired is not None:
        now = datetime.utcnow()

        if expired:
            clients = [c for c in clients if c.expires_at < now]
        else:
            clients = [c for c in clients if c.expires_at >= now]

    return clients


# Получение клиента по id
async def get_client(client_id: UUID) -> SClientResponse:
    client = await crud.get_client(client_id=client_id)

    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    
    return client


# Удаление клиента
async def delete_client(client_id: UUID) -> None:
    client = await crud.get_client(client_id=client_id)

    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    
    await crud.delete_client(client=client)


# Продление подписки
async def extend_client(
    client_id: UUID, 
    days: int
) -> None:
    client = await crud.get_client(client_id=client_id)
    
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    
    return await crud.extend_client(client=client, days=days)


# Блокировка клиента
async def block_client(client_id: UUID) -> None:
    client = await crud.get_client(client_id=client_id)

    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    
    await crud.block_client(client=client)


# Разблокировка клиента
async def unblock_client(client_id: UUID) -> None:
    client = await crud.get_client(client_id=client_id)

    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    
    await crud.unblock_client(client=client)

