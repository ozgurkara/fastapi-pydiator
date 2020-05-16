from pydantic import BaseModel, Field
from app.pydiator.interfaces import BaseRequest, BaseResponse, BaseHandler
from app.pydiator.mediatr import pydiator
from app.db.fake_db import fake_todo_db
from app.resources.todo.handlers.notifications.todo_cache_remove_handler import TodoChangeNotification


class AddTodoRequest(BaseModel, BaseRequest):
    title: str = Field("", title="The title of the item", max_length=300, min_length=1)


class AddTodoResponse(BaseModel, BaseResponse):
    success: bool = Field(...)


class AddTodoHandler(BaseHandler):

    async def handle(self, req: AddTodoRequest) -> AddTodoResponse:
        fake_todo_db.append({
            "id": len(fake_todo_db) + 1,
            "title": req.title
        })

        await pydiator.publish(TodoChangeNotification())

        return AddTodoResponse(success=True)
