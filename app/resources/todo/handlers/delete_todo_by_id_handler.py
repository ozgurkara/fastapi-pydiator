from pydantic import BaseModel, Field
from app.pydiator.mediatr import pydiator
from app.pydiator.interfaces import BaseRequest, BaseResponse, BaseHandler
from app.db.fake_db import fake_todo_db
from app.resources.todo.handlers.notifications.todo_cache_remove_handler import TodoChangeNotification


class DeleteTodoByIdRequest(BaseModel, BaseRequest):
    id: int = Field(0, gt=0, title="item id")


class DeleteTodoByIdResponse(BaseModel, BaseResponse):
    success: bool = Field(...)


class DeleteTodoByIdHandler(BaseHandler):

    async def handle(self, req: DeleteTodoByIdRequest) -> DeleteTodoByIdResponse:
        for it in fake_todo_db:
            if it["id"] == req.id:
                fake_todo_db.remove(it)
                await pydiator.publish(TodoChangeNotification())

                return DeleteTodoByIdResponse(success=True)

        return DeleteTodoByIdResponse(success=False)
