import asyncio
from unittest import TestCase

from pydiator_core.mediatr_container import MediatrContainer
from pydiator_core.mediatr import pydiator


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
        pydiator.ready(container=container)
