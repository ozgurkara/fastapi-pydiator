import traceback
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from starlette import status
from starlette.responses import JSONResponse

from app.utils.error.error_response import ErrorResponse, ErrorsInfoStack


def unhandled_exception_handler(request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=generate_error_content(
            error_info=ErrorsInfoStack.unhandled_error,
            error_detail=[generate_stack_trace(exc)]
        ),
    )


def http_exception_handler(request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=generate_error_content(
            error_info=ErrorsInfoStack.unhandled_error,
            error_detail=[exc.detail]
        ),
    )


def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=generate_error_content(
            error_info=ErrorsInfoStack.model_validation_error,
            error_detail=exc.errors()
        ),
    )


def generate_error_content(error_info: ErrorsInfoStack.ErrorInfo, error_detail: list):
    return jsonable_encoder(
        ErrorResponse(
            error_code=error_info.code,
            error_message=error_info.message,
            error_detail=error_detail,
        ).dict()
    )


def generate_stack_trace(exc: Exception) -> str:
    return "".join(traceback.TracebackException.from_exception(exc).format())
