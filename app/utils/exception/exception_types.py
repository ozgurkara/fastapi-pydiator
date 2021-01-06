from app.utils.error.error_models import ErrorInfoModel


class ApplicationException(Exception):
    def __init__(self, error_info: ErrorInfoModel, exception: Exception = None) -> None:
        super().__init__()
        self.exception = exception
        self.error_info = error_info


class DataException(ApplicationException):
    pass


class ServiceException(ApplicationException):
    pass
