import asyncio
from unittest import TestCase, mock


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
