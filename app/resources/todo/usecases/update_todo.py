from pydantic import BaseModel, Field, Extra

from app.data.todo.usecases.update_todo_data import UpdateTodoDataRequest
from pydiator_core.interfaces import BaseRequest, BaseResponse, BaseHandler
from pydiator_core.mediatr import pydiator
from app.resources.todo.notifications.todo_cache_remove_handler import TodoChangeNotification


class UpdateTodoRequest(BaseModel, BaseRequest):
    title: str = Field("", title="The title of the item", max_length=300, min_length=1)

    class CustomFields:
        id: int = Extra.allow


class UpdateTodoResponse(BaseModel, BaseResponse):
    success: bool = Field(...)


class UpdateTodoUseCase(BaseHandler):

    async def handle(self, req: UpdateTodoRequest) -> UpdateTodoResponse:
        data_response = await pydiator.send(UpdateTodoDataRequest(id=req.CustomFields.id, title=req.title))
        if data_response.success:
            await pydiator.publish(TodoChangeNotification())
            return UpdateTodoResponse(success=True)

        return UpdateTodoResponse(success=False)
