from pydantic import BaseModel, Field

from app.data.handlers.todo.delete_todo_by_id_data_handler import DeleteTodoByIdDataRequest
from app.pydiator.mediatr import pydiator
from app.pydiator.interfaces import BaseRequest, BaseResponse, BaseHandler
from app.resources.todo.handlers.notifications.todo_cache_remove_handler import TodoChangeNotification


class DeleteTodoByIdRequest(BaseModel, BaseRequest):
    id: int = Field(0, gt=0, title="item id")


class DeleteTodoByIdResponse(BaseModel, BaseResponse):
    success: bool = Field(...)


class DeleteTodoByIdHandler(BaseHandler):

    async def handle(self, req: DeleteTodoByIdRequest) -> DeleteTodoByIdResponse:
        data_response = await pydiator.send(DeleteTodoByIdDataRequest(id=req.id))
        if data_response:
            await pydiator.publish(TodoChangeNotification())
            return DeleteTodoByIdResponse(success=True)

        return DeleteTodoByIdResponse(success=False)
