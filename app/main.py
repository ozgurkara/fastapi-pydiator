import uvicorn
from app.resources.todo import todo_resource
from pydantic import ValidationError
from fastapi import FastAPI
from fastapi.exception_handlers import (
    http_exception_handler,
    request_validation_exception_handler
)

from app.pydiator_config import set_up_pydiator
from starlette.exceptions import HTTPException as StarletteHTTPException

app = FastAPI()


@app.get("/")
async def home():
    return "hello pydiator"


@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request, exc):
    print(f"OMG! An HTTP error!: {exc}")
    return await http_exception_handler(request, exc)


@app.exception_handler(ValidationError)
async def validation_exception_handler(request, exc):
    return await request_validation_exception_handler(request, exc)


app.include_router(
    todo_resource.router,
    prefix="/v1/todo",
    tags=["todo"]
)

set_up_pydiator()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
