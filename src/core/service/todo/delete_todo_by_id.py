from pydantic import BaseModel, Field

from pydiator_core.mediatr import pydiator
from pydiator_core.interfaces import BaseRequest, BaseResponse, BaseHandler

from src.core.port.repository.todo_repository_port import TodoRepositoryPort
from src.notification.todo_transaction.transaction_notification import TodoTransactionNotification


class DeleteTodoByIdRequest(BaseModel, BaseRequest):
    id: int = Field(0, gt=0, title="item id")


class DeleteTodoByIdResponse(BaseModel, BaseResponse):
    success: bool = Field(...)


class DeleteTodoByIdUseCase(BaseHandler):
    _repository: TodoRepositoryPort = None

    def __init__(self, repository: TodoRepositoryPort):
        self._repository = repository

    async def handle(self, req: DeleteTodoByIdRequest) -> DeleteTodoByIdResponse:
        data_response = await self._repository.delete(req.id)
        if data_response:
            await pydiator.publish(TodoTransactionNotification(id=req.id))
            return DeleteTodoByIdResponse(success=True)

        return DeleteTodoByIdResponse(success=False)
