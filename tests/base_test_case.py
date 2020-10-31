import asyncio
from unittest import TestCase, mock

from app.pydiator.interfaces import BaseRequest, BaseResponse, BaseHandler, BasePipeline, BaseNotification, \
    BaseNotificationHandler
from app.pydiator.mediatr_container import MediatrContainer
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
    pass


class TestResponse(BaseResponse):
    pass


class TestHandler(BaseHandler):
    async def handle(self, req: BaseRequest):
        return TestResponse()


class TestPipeline(BasePipeline):
    async def handle(self, req: BaseRequest) -> object:
        pass


class TestNotification(BaseNotification):
    pass


class TestNotificationHandler(BaseNotificationHandler):

    async def handle(self, notification: BaseNotification):
        pass
