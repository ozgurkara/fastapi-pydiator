from pydantic import BaseModel, Field
from pydiator_core.interfaces import BaseRequest, BaseResponse, BaseHandler
from app.db.fake_db import fake_todo_db
from typing import List


class GetTodoAllDataRequest(BaseModel, BaseRequest):
    def __init__(self):
        pass


class GetTodoAllDataResponse(BaseModel, BaseResponse):
    id: int = Field(...)
    title: str = Field(...)


class GetTodoAllDataUseCase(BaseHandler):

    async def handle(self, req: GetTodoAllDataRequest) -> List[GetTodoAllDataResponse]:
        response = []
        for it in fake_todo_db:
            response.append(GetTodoAllDataResponse(id=it["id"], title=it["title"]))

        return response
