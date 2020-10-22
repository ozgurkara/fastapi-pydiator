from pydantic import BaseModel, Field
from app.pydiator.interfaces import BaseRequest, BaseResponse, BaseHandler
from app.resources.pydiator_config import pydiator
from app.data.handlers.todo.get_todo_by_id_handler import GetTodoByIdDataRequest


class GetTodoByIdRequest(BaseModel, BaseRequest):
    id: int = Field(0, gt=0, description="The item id be greater than zero")


class GetTodoByIdResponse(BaseModel, BaseResponse):
    id: int = Field(...)
    title: str = Field(...)


class GetTodoByIdHandler(BaseHandler):

    async def handle(self, req: GetTodoByIdRequest) -> GetTodoByIdResponse:
        todo_data = await pydiator.send(GetTodoByIdDataRequest(id=req.id))
        if todo_data is not None:
            return GetTodoByIdResponse(id=todo_data.id, title=todo_data.title)

        return None
