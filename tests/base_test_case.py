import asyncio
from typing import List
from unittest import TestCase, mock

from app.pydiator.interfaces import BaseRequest, BaseResponse, BaseHandler, BasePipeline, BaseNotification, \
    BaseNotificationHandler, BaseCacheable, CacheType
from app.pydiator.mediatr_container import MediatrContainer, BaseMediatrContainer
from app.pydiator.mediatr import pydiator


class BaseTestCase(TestCase):
    @staticmethod
    def async_return(result):
        f = asyncio.Future()
        f.set_result(result)
        return f

    @staticmethod
    def async_loop(func):
        loop = asyncio.new_event_loop()
        response = loop.run_until_complete(func)
        loop.close()
        return response

    @staticmethod
    def register_request(req, handler):
        container = MediatrContainer()
        container.register_request(req, handler)
        pydiator.ready(container)


class TestRequest(BaseRequest):
    def __init__(self):
        return


class TestRequestWithCacheable(BaseRequest, BaseCacheable):
    def __init__(self, cache_key, cache_duration, cache_type: CacheType):
        self.cache_key = cache_key
        self.cache_duration = cache_duration
        self.cache_type = cache_type

    def get_cache_key(self) -> str:
        return self.cache_key

    def get_cache_duration(self) -> int:
        return self.cache_duration

    def get_cache_type(self) -> CacheType:
        return self.cache_type


class TestResponse(BaseResponse):
    def __init__(self, success: bool):
        self.success = success


class TestHandler(BaseHandler):
    async def handle(self, req: BaseRequest):
        return TestResponse(success=True)


class TestPipeline(BasePipeline):
    def __init__(self, response_success):
        self.response_success = response_success

    async def handle(self, req: BaseRequest) -> object:
        return TestResponse(success=self.response_success)


class TestNotification(BaseNotification):
    def __init__(self):
        return


class TestNotificationHandler(BaseNotificationHandler):

    async def handle(self, notification: BaseNotification):
        return


class FakeMediatrContainer(BaseMediatrContainer):

    def prepare_pipes(self, pipeline: BasePipeline):
        self.__pipelines.append(pipeline)

    def __init__(self):
        self.__requests = {}
        self.__notifications = {}
        self.__pipelines = []

    def register_request(self, req: BaseRequest, handler: BaseHandler):
        return

    def register_pipeline(self, pipeline: BasePipeline):
        self.__pipelines.append(pipeline)

    def register_notification(self, notification: BaseNotification, handlers: List[BaseNotificationHandler]):
        return

    def get_requests(self):
        return self.__requests

    def get_notifications(self):
        return self.__notifications

    def get_pipelines(self):
        return self.__pipelines
