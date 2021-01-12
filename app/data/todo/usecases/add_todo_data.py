from pydantic import BaseModel, Field
from pydiator_core.interfaces import BaseRequest, BaseResponse, BaseHandler
from app.db.fake_db import fake_todo_db


class AddTodoDataRequest(BaseModel, BaseRequest):
    title: str = Field("", title="The title of the item", max_length=300, min_length=1)


class AddTodoDataResponse(BaseModel, BaseResponse):
    success: bool = Field(...)
    id: int = Field(0, title="todo id")


class AddTodoDataUseCase(BaseHandler):

    async def handle(self, req: AddTodoDataRequest) -> AddTodoDataResponse:
        id = 1
        last_item = fake_todo_db[len(fake_todo_db) - 1]
        if last_item is not None:
            id = last_item["id"] + 1

        fake_todo_db.append({
            "id": id,
            "title": f"title {id}"
        })

        return AddTodoDataResponse(success=True, id=id)
