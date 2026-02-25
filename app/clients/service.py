from fastapi import HTTPException
from uuid import UUID

from app.clients import crud
from app.clients.models import ClientStatus
from app.clients.shemas import SClientResponse, SClientCreate
from app.operations import service


# Создание клиента
async def create_client(days: int = 30) -> SClientCreate:
    if days <= 0:
        raise HTTPException(status_code=404, detail='Days must be positive')
    
    client = await crud.create_client(days=days)
    await service.log_operation(
        client_id=client.id,
        action='create',
        payload={'initial_days': days},
        success=True
    )
    return SClientCreate(id=client.id)


# Получение всех клиентов
async def list_clients(
    status: ClientStatus | None = None,
    expired: bool | None = None
) -> list[SClientResponse]:
    clients = await crud.list_clients(status=status, expired=expired)
    result = [c for c in clients]

    return result


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
    client = await crud.extend_client(client_id=client_id, days=days)
    await service.log_operation(
        client_id=client_id,
        action='extend',
        payload={'days_added': days, 'new_expires_at': client.expires_at.isoformat()},
        success=True
    )

    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    
    return client


# Блокировка клиента
async def block_client(client_id: UUID) -> None:
    client = await crud.block_client(client_id=client_id)

    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    
    await service.log_operation(
        client_id=client_id,
        action='block',
        payload={},
        success=True
    )
    
    return client


# Разблокировка клиента
async def unblock_client(client_id: UUID) -> None:
    client = await crud.unblock_client(client_id=client_id)

    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    
    await service.log_operation(
        client_id=client_id,
        action='unblock',
        payload={},
        success=True
    )
    
    return client


