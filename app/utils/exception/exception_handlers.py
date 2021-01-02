import traceback
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from starlette import status
from starlette.responses import JSONResponse

from app.utils.error.error_response import ErrorResponseModel, ErrorsInfoStack


class ExceptionHandlers:

    @staticmethod
    def unhandled_exception(request, exc: Exception):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=ExceptionHandlers.__get_error_content(
                error_info=ErrorsInfoStack.unhandled_error,
                error_detail=[ExceptionHandlers.__get_stack_trace(exc)]
            ),
        )

    @staticmethod
    def http_exception(request, exc: HTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content=ExceptionHandlers.__get_error_content(
                error_info=ErrorsInfoStack.unhandled_error,
                error_detail=[exc.detail]
            ),
        )

    @staticmethod
    def validation_exception(request, exc):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=ExceptionHandlers.__get_error_content(
                error_info=ErrorsInfoStack.model_validation_error,
                error_detail=exc.errors()
            ),
        )

    @staticmethod
    def __get_error_content(error_info: ErrorsInfoStack.ErrorInfo, error_detail: list):
        return jsonable_encoder(
            ErrorResponseModel(
                error_code=error_info.code,
                error_message=error_info.message,
                error_detail=error_detail,
            ).dict()
        )

    @staticmethod
    def __get_stack_trace(exc: Exception) -> str:
        return "".join(traceback.TracebackException.from_exception(exc).format())
