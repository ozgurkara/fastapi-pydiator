from pydantic import BaseModel, Field, Extra

from src.core.port.repository.todo_repository_port import TodoRepositoryPort
from src.infra.adapter.repository.todo.model.update_models import UpdateTodoInputModel
from pydiator_core.interfaces import BaseRequest, BaseResponse, BaseHandler
from pydiator_core.mediatr import pydiator
from src.notification.todo_transaction.transaction_notification import TodoTransactionNotification


class UpdateTodoRequest(BaseModel, BaseRequest):
    title: str = Field("", title="The title of the item", max_length=300, min_length=1)

    class CustomFields:
        id: int = Extra.allow


class UpdateTodoResponse(BaseModel, BaseResponse):
    success: bool = Field(...)


class UpdateTodoUseCase(BaseHandler):
    _repository: TodoRepositoryPort = None

    def __init__(self, repository: TodoRepositoryPort):
        self._repository = repository

    async def handle(self, req: UpdateTodoRequest) -> UpdateTodoResponse:
        data_response = await self._repository.update(UpdateTodoInputModel(id=req.CustomFields.id, title=req.title))
        if data_response.success:
            await pydiator.publish(TodoTransactionNotification(id=req.CustomFields.id))
            return UpdateTodoResponse(success=True)

        return UpdateTodoResponse(success=False)
