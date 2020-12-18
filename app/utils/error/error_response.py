from typing import List
from app.utils.error.error_models import ErrorsInfoStack, ErrorResponse


def generate_error_response():
    return {
        "application/json": {
            "example": ErrorResponse(
                error_code=ErrorsInfoStack.could_not_get_excepted_response.code,
                error_message=ErrorsInfoStack.could_not_get_excepted_response.message
            ).dict()
        }
    }


def generate_validation_error_response(invalid_field_location: List[str]):
    return {
        "application/json": {
            "example": ErrorResponse(
                error_code=ErrorsInfoStack.model_validation_error.code,
                error_message=ErrorsInfoStack.model_validation_error.message,
                error_detail=generate_error_detail(
                    error_location=invalid_field_location
                ),
            ).dict()
        }
    }


def generate_error_detail(error_location: List[str]):
    return [
        {
            "loc": error_location,
            "msg": "field required",
            "type": "value_error.missing",
        }
    ]
