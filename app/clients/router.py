from fastapi import APIRouter, Query, status
from uuid import UUID

from app.clients import service
from app.clients.models import ClientStatus
from app.clients.shemas import SClientResponse, SClientCreate, SClientExtend


router = APIRouter(prefix='/clients', tags=['Clients'])


# Эндпоинт создания клиента
@router.post('/create', status_code=status.HTTP_201_CREATED)
async def create_client() -> SClientCreate:
    return await service.create_client()


# Эндпоинт для получения всех клиентов
@router.get('/', status_code=status.HTTP_200_OK)
async def list_clients(
    status: ClientStatus | None = Query(None),
    expired: bool | None = Query(None)
) -> list[SClientResponse]:
    return await service.list_clients(status, expired)


# Эндпоинт для получения клиента по id
@router.get('/{client_id}', status_code=status.HTTP_200_OK)
async def get_client(client_id: UUID) -> SClientResponse:
    return await service.get_client(client_id)


# Эндпоинт удаления клиента
@router.delete('/{client_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_client(client_id: UUID) -> None:
    await service.delete_client(client_id)


# Эндпоинт продления подписки клиента
@router.post('/{client_id}/extend', status_code=status.HTTP_200_OK)
async def extend_client(
    client_id: UUID,
    body: SClientExtend
) -> None:
    await service.extend_client(client_id, body.days)


# Эндпоинт блокировки клиента
@router.post('/{client_id}/block', status_code=status.HTTP_200_OK)
async def block_client(client_id: UUID) -> None:
    await service.block_client(client_id)


# Эндпоинт разблокировки клиента
@router.post('/{client_id}/unblock', status_code=status.HTTP_200_OK)
async def unblock_client(client_id: UUID) -> None:
    await service.unblock_client(client_id)