from pydantic import BaseModel, Field
from app.pydiator.interfaces import BaseRequest, BaseResponse, BaseHandler, BaseCacheable, CacheType
from app.db.fake_db import fake_todo_db


class GetTodoByIdRequest(BaseModel, BaseRequest):
    id: int = Field(0, gt=0, description="The item id be greater than zero")


class GetTodoByIdResponse(BaseModel, BaseResponse):
    id: int = Field(...)
    title: str = Field(...)


class GetTodoByIdHandler(BaseHandler):

    async def handle(self, req: GetTodoByIdRequest) -> GetTodoByIdResponse:
        for it in fake_todo_db:
            if it["id"] == req.id:
                return GetTodoByIdResponse(id=it["id"], title=it["title"])

        return None
