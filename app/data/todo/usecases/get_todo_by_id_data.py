from pydantic import BaseModel, Field
from pydiator_core.interfaces import BaseRequest, BaseResponse, BaseHandler
from app.db.fake_db import fake_todo_db


class GetTodoByIdDataRequest(BaseModel, BaseRequest):
    id: int = Field(0, gt=0, description="The item id be greater than zero")


class GetTodoByIdDataResponse(BaseModel, BaseResponse):
    id: int = Field(...)
    title: str = Field(...)


class GetTodoByIdDataUseCase(BaseHandler):

    async def handle(self, req: GetTodoByIdDataRequest) -> GetTodoByIdDataResponse:
        for it in fake_todo_db:
            if it["id"] == req.id:
                return GetTodoByIdDataResponse(id=it["id"], title=it["title"])

        return None
