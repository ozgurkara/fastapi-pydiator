from pydantic import BaseModel, Field
from pydiator_core.interfaces import BaseRequest, BaseResponse, BaseHandler
from app.db.fake_db import fake_todo_db


class DeleteTodoByIdDataRequest(BaseModel, BaseRequest):
    id: int = Field(0, gt=0, title="item id")


class DeleteTodoByIdDataResponse(BaseModel, BaseResponse):
    success: bool = Field(...)


class DeleteTodoByIdDataUseCase(BaseHandler):

    async def handle(self, req: DeleteTodoByIdDataRequest) -> DeleteTodoByIdDataResponse:
        for it in fake_todo_db:
            if it["id"] == req.id:
                fake_todo_db.remove(it)
                return DeleteTodoByIdDataResponse(success=True)

        return DeleteTodoByIdDataResponse(success=False)
