from pydantic import BaseModel, Field

from pydiator_core.interfaces import BaseRequest, BaseResponse, BaseHandler
from pydiator_core.mediatr import pydiator

from src.core.port.repository.todo_repository_port import TodoRepositoryPort
from src.notification.todo_transaction.transaction_notification import TodoTransactionNotification
from src.infra.adapter.repository.todo.model.add_models import AddTodoInputModel, AddTodoOutputModel


class AddTodoRequest(BaseModel, BaseRequest):
    title: str = Field("title", title="The title of the item", max_length=300, min_length=1)


class AddTodoResponse(BaseModel, BaseResponse):
    success: bool = Field(...)


class AddTodoUseCase(BaseHandler):
    _repository: TodoRepositoryPort = None

    def __init__(self, repository: TodoRepositoryPort):
        self._repository = repository

    async def handle(self, req: AddTodoRequest) -> AddTodoResponse:
        data_response: AddTodoOutputModel = await self._repository.add(AddTodoInputModel(title=req.title))
        if data_response.success:
            await pydiator.publish(TodoTransactionNotification(id=data_response.id))
            return AddTodoResponse(success=True)

        return AddTodoResponse(success=False)
