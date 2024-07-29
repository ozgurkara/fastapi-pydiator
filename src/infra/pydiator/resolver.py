from src.core.service.todo.add_todo import AddTodoUseCase
from src.core.service.todo.delete_todo_by_id import DeleteTodoByIdUseCase
from src.core.service.todo.get_todo_all import GetTodoAllUseCase
from src.core.service.todo.get_todo_by_id import GetTodoByIdUseCase
from src.core.service.todo.update_todo import UpdateTodoUseCase
from src.infra.adapter.repository.todo.in_memory_todo_repository import InMemoryTodoRepository


class TodoResolver:

    @staticmethod
    def get_todo_all_resolver():
        return GetTodoAllUseCase(repository=InMemoryTodoRepository())

    @staticmethod
    def get_todo_by_id_resolver():
        return GetTodoByIdUseCase(repository=InMemoryTodoRepository())

    @staticmethod
    def add_todo_resolver():
        return AddTodoUseCase(repository=InMemoryTodoRepository())

    @staticmethod
    def update_todo_resolver():
        return UpdateTodoUseCase(repository=InMemoryTodoRepository())

    @staticmethod
    def delete_todo_resolver():
        return DeleteTodoByIdUseCase(repository=InMemoryTodoRepository())
