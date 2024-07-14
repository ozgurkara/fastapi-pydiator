from pydantic import ValidationError
from starlette.exceptions import HTTPException

from src.api.controller.health_check import health_check_controller
from src.api.controller.todo import todo_controller
from fastapi import FastAPI

from src.infra.exception.exception_handlers import ExceptionHandlers
from src.infra.exception.exception_types import DataException, ServiceException
from src.infra.pydiator.pydiator_core_config import set_up_pydiator



def create_app():
    app = FastAPI(
        title="FastAPI Pydiator",
        description="FastAPI pydiator integration project",
        version="1.0.0",
        openapi_url="/openapi.json",
        docs_url="/",
        redoc_url="/redoc"
    )

    app.add_exception_handler(Exception, ExceptionHandlers.unhandled_exception)
    app.add_exception_handler(DataException, ExceptionHandlers.data_exception)
    app.add_exception_handler(ServiceException, ExceptionHandlers.service_exception)
    app.add_exception_handler(HTTPException, ExceptionHandlers.http_exception)
    app.add_exception_handler(ValidationError, ExceptionHandlers.validation_exception)

    app.include_router(
        health_check_controller.router,
        prefix="/health-check",
        tags=["health check"]
    )

    app.include_router(
        todo_controller.router,
        prefix="/v1/todos",
        tags=["todo"]
    )

    set_up_pydiator()

    return app
