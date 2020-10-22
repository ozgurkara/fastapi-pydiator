import asyncio
from unittest import TestCase, mock


class BaseTestCase(TestCase):
    @staticmethod
    def async_return(result):
        f = asyncio.Future()
        f.set_result(result)
        return f
