from pydantic import BaseModel


class UpdateTodoInputModel(BaseModel):
    title: str
    id: int


class UpdateTodoOutputModel(BaseModel):
    success: bool
