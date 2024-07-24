from abc import abstractmethod, ABC
from typing import List

from src.infra.adapter.repository.todo.model.add_models import AddTodoInputModel, AddTodoOutputModel
from src.infra.adapter.repository.todo.model.get_all_models import GetAllTodoOutputModel
from src.infra.adapter.repository.todo.model.get_by_id_models import GetByIdTodoOutputModel
from src.infra.adapter.repository.todo.model.update_models import UpdateTodoInputModel


class TodoRepositoryPort(ABC):
    @abstractmethod
    async def add(self, add_todo_input_model: AddTodoInputModel) -> AddTodoOutputModel:
        pass

    @abstractmethod
    async def get_by_id(self, id: int) -> GetByIdTodoOutputModel:
        pass

    @abstractmethod
    async def gel_all(self) -> List[GetAllTodoOutputModel]:
        pass

    @abstractmethod
    async def update(self, update_todo_input_model: UpdateTodoInputModel):
        pass

    @abstractmethod
    async def delete(self, id: int) -> bool:
        pass
