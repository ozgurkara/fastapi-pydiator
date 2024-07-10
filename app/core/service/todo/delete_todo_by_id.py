from pydantic import BaseModel, Field

from app.data.todo.usecases.delete_todo_by_id_data import DeleteTodoByIdDataRequest
from pydiator_core.mediatr import pydiator
from pydiator_core.interfaces import BaseRequest, BaseResponse, BaseHandler
from app.notification.todo_transaction.transaction_notification import TodoTransactionNotification


class DeleteTodoByIdRequest(BaseModel, BaseRequest):
    id: int = Field(0, gt=0, title="item id")


class DeleteTodoByIdResponse(BaseModel, BaseResponse):
    success: bool = Field(...)


class DeleteTodoByIdUseCase(BaseHandler):

    async def handle(self, req: DeleteTodoByIdRequest) -> DeleteTodoByIdResponse:
        data_response = await pydiator.send(DeleteTodoByIdDataRequest(id=req.id))
        if data_response.success:
            await pydiator.publish(TodoTransactionNotification(id=req.id))
            return DeleteTodoByIdResponse(success=True)

        return DeleteTodoByIdResponse(success=False)
