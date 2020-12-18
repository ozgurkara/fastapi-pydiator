import uvicorn
from pydantic import ValidationError
from starlette.exceptions import HTTPException

from app.resources.todo import todo_resource
from fastapi import FastAPI
from app.utils.exception.exception_handlers import http_exception_handler, validation_exception_handler, \
    unhandled_exception_handler
from app.pydiator_core_config import set_up_pydiator

app = FastAPI()


def add_exception_handlers(a: FastAPI):
    a.add_exception_handler(Exception, unhandled_exception_handler)
    a.add_exception_handler(HTTPException, http_exception_handler)
    a.add_exception_handler(ValidationError, validation_exception_handler)


@app.get("/")
async def home():
    return "hello pydiator"


app.include_router(
    todo_resource.router,
    prefix="/v1/todos",
    tags=["todo"]
)

add_exception_handlers(app)
set_up_pydiator()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8001, log_level="info", reload=True)
