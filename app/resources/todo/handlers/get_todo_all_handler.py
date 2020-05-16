from pydantic import BaseModel, Field
from app.pydiator.interfaces import BaseRequest, BaseResponse, BaseHandler, BaseCacheable, CacheType
from app.db.fake_db import fake_todo_db
from typing import List


class GetTodoAllRequest(BaseModel, BaseRequest, BaseCacheable):
    def get_cache_key(self) -> str:
        return type(self).__name__

    def get_cache_duration(self) -> int:
        return 600

    def get_cache_type(self) -> CacheType:
        return CacheType.DISTRIBUTED


class GetTodoAllResponse(BaseModel, BaseResponse):
    id: int = Field(...)
    title: str = Field(...)


class GetTodoAllHandler(BaseHandler):

    async def handle(self, req: GetTodoAllRequest) -> List[GetTodoAllResponse]:
        response = []
        for it in fake_todo_db:
            response.append(GetTodoAllResponse(id=it["id"], title=it["title"]))

        return response
