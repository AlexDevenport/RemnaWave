from uuid import UUID

from app.operations import crud
from app.operations.models import Operation
from app.operations.shemas import SOperationResponse


# Логирование операции
async def log_operation(
    client_id: UUID,
    action: str,
    payload: dict | None = None,
    success: bool = True,
    error: str | None = None
) -> SOperationResponse:
    op = Operation(
        client_id=client_id,
        action=action,
        payload=payload,
        result='success' if success else 'fail',
        error=error if not success else None
    )
    created = await crud.create_operation(op)
    return SOperationResponse.from_orm(created)


# Список операций
async def list_operations(client_id: UUID | None = None) -> list[SOperationResponse]:
    operations = await crud.list_operations(client_id=client_id)
    return operations