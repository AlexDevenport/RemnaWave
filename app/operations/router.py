from fastapi import APIRouter, Query, status
from uuid import UUID

from app.operations import service
from app.operations.shemas import SOperationResponse


router = APIRouter(prefix='/operations', tags=['Operations'])


# Эндпоинт списка всех операций над клиентом
@router.get('/', status_code=status.HTTP_200_OK)
async def get_operations(client_id: UUID | None = Query(None)) -> list[SOperationResponse]:
    return await service.list_operations(client_id=client_id)
