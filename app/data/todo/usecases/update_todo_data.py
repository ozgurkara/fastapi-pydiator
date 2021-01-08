from pydantic import BaseModel, Field, Extra
from pydiator_core.interfaces import BaseRequest, BaseResponse, BaseHandler
from app.db.fake_db import fake_todo_db
from app.utils.error.error_models import ErrorInfoContainer
from app.utils.exception.exception_types import DataException


class UpdateTodoDataRequest(BaseModel, BaseRequest):
    title: str = Field("", title="The title of the item", max_length=300, min_length=1)
    id: int = Field(0, title="", gt=0)


class UpdateTodoDataResponse(BaseModel, BaseResponse):
    success: bool = Field(...)


class UpdateTodoDataUseCase(BaseHandler):

    async def handle(self, req: UpdateTodoDataRequest) -> UpdateTodoDataResponse:
        for it in fake_todo_db:
            if it["id"] == req.id:
                it["title"] = req.title
                return UpdateTodoDataResponse(success=True)

        raise DataException(error_info=ErrorInfoContainer.todo_not_found_error)

