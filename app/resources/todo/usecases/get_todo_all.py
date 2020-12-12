from pydantic import BaseModel, Field
from pydiator_core.interfaces import BaseRequest, BaseResponse, BaseHandler, BaseCacheable, CacheType
from typing import List
from pydiator_core.mediatr import pydiator
from app.data.todo.usecases.get_todo_all_data import GetTodoAllDataRequest


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


class GetTodoAllUseCase(BaseHandler):

    async def handle(self, req: GetTodoAllRequest) -> List[GetTodoAllResponse]:
        response = []
        data_response = await pydiator.send(GetTodoAllDataRequest())
        for d in data_response:
            response.append(GetTodoAllResponse(id=d.id, title=d.title))

        return response
