import enum

from abc import ABC, abstractmethod
from typing import List
from app.utils.serializer_helper import JsonSerializable


class BaseRequest:
    def __init__(self):
        pass


class BaseNotification:
    def __init__(self):
        pass


class BaseResponse(JsonSerializable):
    def __init__(self):
        pass


class BaseHandler(ABC):
    def __init__(self):
        pass

    @abstractmethod
    async def handle(self, req: BaseRequest):
        pass


class BaseNotificationHandler(ABC):
    def __init__(self):
        pass

    @abstractmethod
    async def handle(self, notification: BaseNotification):
        pass


class CacheType(enum.Enum):
    NONE = 0
    DISTRIBUTED = 1
    MEMORY = 2


class BaseCacheable(ABC):

    def __init__(self):
        self._no_cache = False

    @abstractmethod
    def get_cache_key(self) -> str:
        pass

    @abstractmethod
    def get_cache_duration(self) -> int:
        pass

    @abstractmethod
    def get_cache_type(self) -> CacheType:
        pass

    def set_no_cache(self):
        self._no_cache = True

    def is_no_cache(self):
        if hasattr(self, '_no_cache'):
            return self._no_cache
        return False


class BasePipeline(ABC):
    _next = None

    def __init__(self):
        pass

    def next(self) -> object:
        return self._next

    def set_next(self, handler=None):
        self._next = handler

    def has_next(self):
        return self._next is not None

    @abstractmethod
    async def handle(self, req: BaseRequest) -> object:
        pass


class BaseMediatr(ABC):

    @abstractmethod
    async def send(self, req: BaseRequest) -> object:
        pass

    @abstractmethod
    async def publish(self, notification: BaseNotification, throw_exception: bool = False):
        pass


class BaseMediatrContainer(ABC):

    @abstractmethod
    def register_request(self, req: BaseRequest, handler: BaseHandler):
        pass

    @abstractmethod
    def register_pipeline(self, pipeline: BasePipeline):
        pass

    @abstractmethod
    def register_notification(self, notification: BaseNotification, handlers: List[BaseNotificationHandler]):
        pass

    @abstractmethod
    def get_requests(self):
        pass

    @abstractmethod
    def get_notifications(self):
        pass

    @abstractmethod
    def get_pipelines(self):
        pass

    @abstractmethod
    def prepare_pipes(self, pipeline: BasePipeline):
        pass
