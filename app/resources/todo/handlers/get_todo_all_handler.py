from pydantic import BaseModel, Field
from app.pydiator.interfaces import BaseRequest, BaseResponse, BaseHandler, BaseCacheable, CacheType
from typing import List
from app.resources.pydiator_config import pydiator
from app.data.handlers.todo.get_todo_all_data_handler import GetTodoAllDataRequest


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
        data_response = await pydiator.send(GetTodoAllDataRequest())

        for d in data_response:
            response.append(GetTodoAllResponse(id=d.id, title=d.title))

        return response
