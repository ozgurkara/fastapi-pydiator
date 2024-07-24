from pydantic import BaseModel


class AddTodoInputModel(BaseModel):
    title: str


class AddTodoOutputModel(BaseModel):
    success: bool
    id: int
