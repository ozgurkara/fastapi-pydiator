from pydantic import BaseModel


class ErrorsInfoStack:
    class ErrorInfo:
        def __init__(self, code: int, message: str):
            self.code = code
            self.message = message

        def __repr__(self):
            return f'code:{self.code},message:{self.message}'

    # General errors
    unhandled_error = ErrorInfo(code=1, message='Internal server error')
    could_not_get_excepted_response = ErrorInfo(code=2, message='Could not get expected response')
    model_validation_error = ErrorInfo(code=100, message='Model validation error')
    not_found_error = ErrorInfo(code=101, message='Not found')
    # Custom errors


class ErrorResponseModel(BaseModel):
    error_code: int = None
    error_message: str = None
    error_detail: list = None
