import uvicorn
from pydantic import ValidationError
from starlette.exceptions import HTTPException

from app.resources.todo import todo_resource
from fastapi import FastAPI
from app.utils.exception.exception_handlers import ExceptionHandlers
from app.pydiator_core_config import set_up_pydiator


def create_app():
    app = FastAPI(
        title="FastApi Pydiator",
        description="fastapi pydiator example project",
        version="1.0.0",
        openapi_url="/openapi.json",
        docs_url="/",
        redoc_url="/redoc",
    )
    app.add_exception_handler(Exception, ExceptionHandlers.unhandled_exception)
    app.add_exception_handler(HTTPException, ExceptionHandlers.http_exception)
    app.add_exception_handler(ValidationError, ExceptionHandlers.validation_exception)
    app.include_router(
        todo_resource.router,
        prefix="/v1/todos",
        tags=["todo"]
    )

    set_up_pydiator()

    return app