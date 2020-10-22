from pydantic import BaseModel, Field, Extra

from app.data.todo.handlers.update_todo_data_handler import UpdateTodoDataRequest
from app.pydiator.interfaces import BaseRequest, BaseResponse, BaseHandler
from app.pydiator.mediatr import pydiator
from app.resources.todo.handlers.notifications.todo_cache_remove_handler import TodoChangeNotification


class UpdateTodoRequest(BaseModel, BaseRequest):
    title: str = Field("", title="The title of the item", max_length=300, min_length=1)

    class CustomFields:
        id: int = Extra.allow


class UpdateTodoResponse(BaseModel, BaseResponse):
    success: bool = Field(...)


class UpdateTodoHandler(BaseHandler):

    async def handle(self, req: UpdateTodoRequest) -> UpdateTodoResponse:
        data_response = await pydiator.send(UpdateTodoDataRequest(id=req.CustomFields.id, title=req.title))
        if data_response.success:
            await pydiator.publish(TodoChangeNotification())
            return UpdateTodoResponse(success=True)

        return UpdateTodoResponse(success=False)
