from pydantic import BaseModel


class ErrorInfoModel:
    def __init__(self, code: int, message: str):
        self.code = code
        self.message = message

    def __repr__(self):
        return f'code:{self.code},message:{self.message}'


class ErrorInfoContainer:
    # General errors
    unhandled_error = ErrorInfoModel(code=1, message='Internal server error')
    could_not_get_excepted_response = ErrorInfoModel(code=2, message='Could not get expected response')
    model_validation_error = ErrorInfoModel(code=3, message='Model validation error')
    not_found_error = ErrorInfoModel(code=4, message='Not found')

    # Custom errors
    todo_not_found_error = ErrorInfoModel(code=101, message='Todo not found')


class ErrorResponseModel(BaseModel):
    error_code: int = None
    error_message: str = None
    error_detail: list = None
