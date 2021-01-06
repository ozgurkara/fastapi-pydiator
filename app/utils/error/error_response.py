from typing import List
from app.utils.error.error_models import ErrorInfoContainer, ErrorResponseModel


class ErrorResponseExample:

    @staticmethod
    def get_error_response():
        return {
            "application/json": {
                "example": ErrorResponseModel(
                    error_code=ErrorInfoContainer.could_not_get_excepted_response.code,
                    error_message=ErrorInfoContainer.could_not_get_excepted_response.message
                ).dict()
            }
        }

    @staticmethod
    def get_validation_error_response(invalid_field_location: List[str]):
        return {
            "application/json": {
                "example": ErrorResponseModel(
                    error_code=ErrorInfoContainer.model_validation_error.code,
                    error_message=ErrorInfoContainer.model_validation_error.message,
                    error_detail=[{
                        "loc": invalid_field_location,
                        "msg": "field required",
                        "type": "value_error.missing",
                    }]
                ).dict()
            }
        }
