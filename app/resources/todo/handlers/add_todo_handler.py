from pydantic import BaseModel, Field

from app.data.todo.handlers.add_todo_data_handler import AddTodoDataRequest
from pydiator_core.interfaces import BaseRequest, BaseResponse, BaseHandler
from pydiator_core.mediatr import pydiator
from app.resources.todo.notifications.todo_cache_remove_handler import TodoChangeNotification


class AddTodoRequest(BaseModel, BaseRequest):
    title: str = Field("", title="The title of the item", max_length=300, min_length=1)


class AddTodoResponse(BaseModel, BaseResponse):
    success: bool = Field(...)


class AddTodoHandler(BaseHandler):

    async def handle(self, req: AddTodoRequest) -> AddTodoResponse:
        data_response = await pydiator.send(AddTodoDataRequest(title=req.title))
        if data_response.success:
            await pydiator.publish(TodoChangeNotification())
            return AddTodoResponse(success=True)

        return AddTodoResponse(success=False)
