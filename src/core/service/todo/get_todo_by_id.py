from pydantic import BaseModel, Field
from pydiator_core.interfaces import BaseRequest, BaseResponse, BaseHandler

from src.infra.adapter.repository.todo.todo_repository import TodoRepository
from src.infra.util.error.error_models import ErrorInfoContainer
from src.infra.exception.exception_types import ServiceException


class GetTodoByIdRequest(BaseModel, BaseRequest):
    id: int = Field(0, gt=0, description="The item id be greater than zero")


class GetTodoByIdResponse(BaseModel, BaseResponse):
    id: int = Field(...)
    title: str = Field(...)


class GetTodoByIdUseCase(BaseHandler):

    async def handle(self, req: GetTodoByIdRequest) -> GetTodoByIdResponse:
        todo_data = await TodoRepository.get_by_id(id=req.id)
        if todo_data is not None:
            return GetTodoByIdResponse(id=todo_data.id, title=todo_data.title)

        raise ServiceException(error_info=ErrorInfoContainer.todo_not_found_error)
