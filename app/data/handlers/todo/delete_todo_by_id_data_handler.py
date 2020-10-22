from pydantic import BaseModel, Field

from app.data.handlers.todo.get_todo_by_id_handler import GetTodoByIdDataRequest
from app.pydiator.interfaces import BaseRequest, BaseResponse, BaseHandler
from app.db.fake_db import fake_todo_db
#from app.resources.pydiator_config import pydiator


class DeleteTodoByIdDataRequest(BaseModel, BaseRequest):
    id: int = Field(0, gt=0, title="item id")


class DeleteTodoByIdDataResponse(BaseModel, BaseResponse):
    success: bool = Field(...)


class DeleteTodoByIdDataHandler(BaseHandler):

    async def handle(self, req: DeleteTodoByIdDataRequest) -> DeleteTodoByIdDataResponse:
        #data_res = await pydiator.send(GetTodoByIdDataRequest(id=1))

        for it in fake_todo_db:
            if it["id"] == req.id:
                fake_todo_db.remove(it)
                return DeleteTodoByIdDataResponse(success=True)

        return DeleteTodoByIdDataResponse(success=False)
