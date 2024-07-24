from pydantic import BaseModel


class GetAllTodoOutputModel(BaseModel):
    id: int
    title: str
