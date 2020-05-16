from pydantic import BaseModel, Field, Extra
from app.pydiator.interfaces import BaseRequest, BaseResponse, BaseHandler
from app.pydiator.mediatr import pydiator
from app.db.fake_db import fake_todo_db
from app.resources.todo.handlers.notifications.todo_cache_remove_handler import TodoChangeNotification


class UpdateTodoRequest(BaseModel, BaseRequest):
    title: str = Field("", title="The title of the item", max_length=300, min_length=1)

    class CustomFields:
        id: int = Extra.allow


class UpdateTodoResponse(BaseModel, BaseResponse):
    success: bool = Field(...)


class UpdateTodoHandler(BaseHandler):

    async def handle(self, req: UpdateTodoRequest) -> UpdateTodoResponse:
        for it in fake_todo_db:
            if it["id"] == req.CustomFields.id:
                it["title"] = req.title
                await pydiator.publish(TodoChangeNotification())
                return UpdateTodoResponse(success=True)

        return UpdateTodoResponse(success=False)
