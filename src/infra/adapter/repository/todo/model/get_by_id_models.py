from pydantic import BaseModel

class GetByIdTodoOutputModel(BaseModel):
    id: int
    title: str
