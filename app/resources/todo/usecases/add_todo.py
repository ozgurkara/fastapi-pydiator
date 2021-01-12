from pydantic import BaseModel, Field

from app.data.todo.usecases.add_todo_data import AddTodoDataRequest, AddTodoDataResponse
from pydiator_core.interfaces import BaseRequest, BaseResponse, BaseHandler
from pydiator_core.mediatr import pydiator
from app.notification.todo_transaction.transaction_notification import TodoTransactionNotification


class AddTodoRequest(BaseModel, BaseRequest):
    title: str = Field("title", title="The title of the item", max_length=300, min_length=1)


class AddTodoResponse(BaseModel, BaseResponse):
    success: bool = Field(...)


class AddTodoUseCase(BaseHandler):

    async def handle(self, req: AddTodoRequest) -> AddTodoResponse:
        data_response: AddTodoDataResponse = await pydiator.send(AddTodoDataRequest(title=req.title))
        if data_response.success:
            await pydiator.publish(TodoTransactionNotification(id=data_response.id))
            return AddTodoResponse(success=True)

        return AddTodoResponse(success=False)
