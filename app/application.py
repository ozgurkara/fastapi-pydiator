from pydantic import ValidationError
from starlette.exceptions import HTTPException
from fastapi_contrib.tracing.middlewares import OpentracingMiddleware

from app.resources.todo import todo_resource
from fastapi import FastAPI
from app.utils.exception.exception_handlers import ExceptionHandlers
from app.pydiator_core_config import set_up_pydiator
from app.utils.exception.exception_types import DataException, ServiceException
from fastapi_contrib.common.middlewares import StateRequestIDMiddleware

from app.utils.tracer_config import tracer


def create_app():
    app = FastAPI(
        title="FastApi Pydiator",
        description="fastapi pydiator example project",
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

    @app.on_event('startup')
    async def startup():
        print("startup")
        app.state.tracer = tracer
        app.tracer = app.state.tracer
        app.add_middleware(OpentracingMiddleware)
        app.add_middleware(StateRequestIDMiddleware)

    app.include_router(
        todo_resource.router,
        prefix="/v1/todos",
        tags=["todo"]
    )

    set_up_pydiator()

    return app
