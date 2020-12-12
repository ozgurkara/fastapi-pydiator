from fastapi import APIRouter
from typing import List
from fastapi import Response, status
from pydiator_core.mediatr import pydiator
from app.resources.todo.usecases.get_todo_all import GetTodoAllRequest, GetTodoAllResponse
from app.resources.todo.usecases.get_todo_by_id import GetTodoByIdRequest, GetTodoByIdResponse
from app.resources.todo.usecases.add_todo import AddTodoRequest, AddTodoResponse
from app.resources.todo.usecases.update_todo import UpdateTodoRequest, UpdateTodoResponse
from app.resources.todo.usecases.delete_todo_by_id import DeleteTodoByIdRequest, DeleteTodoByIdResponse

router = APIRouter()


@router.get("", response_model=List[GetTodoAllResponse], status_code=200)
async def get_todo_all():
    return await pydiator.send(GetTodoAllRequest())


@router.get("/{id}", response_model=GetTodoByIdResponse, status_code=200)
async def get_todo_by_id(id: int, response: Response):
    result = await pydiator.send(GetTodoByIdRequest(id=id))
    if result is None:
        response.status_code = status.HTTP_404_NOT_FOUND

    return result


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
