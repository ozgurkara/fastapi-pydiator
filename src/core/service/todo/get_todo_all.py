from typing import List
from pydantic import BaseModel, Field
from pydiator_core.interfaces import BaseRequest, BaseResponse, BaseHandler, BaseCacheable, CacheType

from src.core.port.repository.todo_repository_port import TodoRepositoryPort


class GetTodoAllRequest(BaseModel, BaseRequest, BaseCacheable):
    def get_cache_key(self) -> str:
        return type(self).__name__

    def get_cache_duration(self) -> int:
        return 600

    def get_cache_type(self) -> CacheType:
        return CacheType.DISTRIBUTED


class Todo(BaseModel):
    id: int = Field(...)
    title: str = Field(...)


class GetTodoAllResponse(BaseModel, BaseResponse):
    items: List[Todo] = []


class GetTodoAllUseCase(BaseHandler):
    _repository: TodoRepositoryPort

    def __init__(self, repository: TodoRepositoryPort):
        self._repository = repository

    async def handle(self, req: GetTodoAllRequest) -> GetTodoAllResponse:
        response = GetTodoAllResponse()
        todo_data = await self._repository.gel_all()
        for item in todo_data:
            response.items.append(Todo(id=item.id, title=item.title))

        return response
