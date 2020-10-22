from fastapi import APIRouter
from typing import List
from app.pydiator.mediatr import pydiator
from app.resources.todo.handlers.get_todo_all_handler import GetTodoAllRequest, GetTodoAllResponse
from app.resources.todo.handlers.get_todo_by_id_handler import GetTodoByIdRequest, GetTodoByIdResponse
from app.resources.todo.handlers.add_todo_handler import AddTodoRequest, AddTodoResponse
from app.resources.todo.handlers.update_todo_handler import UpdateTodoRequest, UpdateTodoResponse
from app.resources.todo.handlers.delete_todo_by_id_handler import DeleteTodoByIdRequest, DeleteTodoByIdResponse

router = APIRouter()


@router.get("", response_model=List[GetTodoAllResponse], status_code=200)
async def get_todo_all():
    return await pydiator.send(GetTodoAllRequest())


@router.get("/{id}", response_model=GetTodoByIdResponse, status_code=200)
async def get_todo_by_id(id: int):
    return await pydiator.send(GetTodoByIdRequest(id=id))


@router.post("", response_model=AddTodoResponse, status_code=200)
async def ad_todo(req: AddTodoRequest):
    return await pydiator.send(req)


@router.put("/{id}", response_model=UpdateTodoResponse, status_code=200)
async def update_todo(id: int, req: UpdateTodoRequest):
    req.CustomFields.id = id
    return await pydiator.send(req)


@router.delete("/{id}", response_model=DeleteTodoByIdResponse, status_code=200)
async def delete_todo(id: int):
    return await pydiator.send(DeleteTodoByIdRequest(id=id))
