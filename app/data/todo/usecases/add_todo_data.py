from pydantic import BaseModel, Field
from pydiator_core.interfaces import BaseRequest, BaseResponse, BaseHandler
from app.db.fake_db import fake_todo_db


class AddTodoDataRequest(BaseModel, BaseRequest):
    title: str = Field("", title="The title of the item", max_length=300, min_length=1)


class AddTodoDataResponse(BaseModel, BaseResponse):
    success: bool = Field(...)


class AddTodoDataUseCase(BaseHandler):

    async def handle(self, req: AddTodoDataRequest) -> AddTodoDataResponse:
        fake_todo_db.append({
            "id": len(fake_todo_db) + 1,
            "title": req.title
        })

        return AddTodoDataResponse(success=True)
