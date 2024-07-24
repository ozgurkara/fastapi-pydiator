from typing import List

from src.core.port.repository.todo_repository_port import TodoRepositoryPort
from src.infra.adapter.repository.fake_db import fake_todo_db
from src.infra.adapter.repository.todo.model.add_models import AddTodoInputModel, AddTodoOutputModel
from src.infra.adapter.repository.todo.model.get_all_models import GetAllTodoOutputModel
from src.infra.adapter.repository.todo.model.get_by_id_models import GetByIdTodoOutputModel
from src.infra.adapter.repository.todo.model.update_models import UpdateTodoInputModel, UpdateTodoOutputModel


class InMemoryTodoRepository(TodoRepositoryPort):
    def __init__(self):
        pass

    async def add(self, add_todo_input_model: AddTodoInputModel) -> AddTodoOutputModel:
        id = 1
        last_item = fake_todo_db[len(fake_todo_db) - 1]
        if last_item is not None:
            id = last_item["id"] + 1

        fake_todo_db.append({
            "id": id,
            "title": f"{add_todo_input_model.title} {id}"
        })
        return AddTodoOutputModel(success=True, id=id)

    async def get_by_id(self, id: int) -> GetByIdTodoOutputModel:
        for it in fake_todo_db:
            if it["id"] == id:
                return GetByIdTodoOutputModel(id=it["id"], title=it["title"])

    async def gel_all(self) -> List[GetAllTodoOutputModel]:
        response = []
        for it in fake_todo_db:
            response.append(GetAllTodoOutputModel(id=it["id"], title=it["title"]))
        return response

    async def update(self, update_todo_input_model: UpdateTodoInputModel):
        for it in fake_todo_db:
            if it["id"] == update_todo_input_model.id:
                it["title"] = update_todo_input_model.title
                return UpdateTodoOutputModel(success=True)

    async def delete(self, id: int) -> bool:
        for it in fake_todo_db:
            if it["id"] == id:
                fake_todo_db.remove(it)
                return True
