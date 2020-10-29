from typing import List
from unittest import mock
from unittest.mock import MagicMock

from app.pydiator.interfaces import BaseNotification, BaseNotificationHandler, BasePipeline, BaseRequest, BaseHandler
from app.pydiator.mediatr import Mediatr
from app.pydiator.mediatr_container import BaseMediatrContainer
from tests.base_test_case import BaseTestCase


class FakeMediatrContainer(BaseMediatrContainer):

    def prepare_pipes(self, pipeline: BasePipeline):
        self.__pipelines.append(pipeline)

    def __init__(self):
        self.__requests = {}
        self.__notifications = {}
        self.__pipelines = []

    def register_request(self, req: BaseRequest, handler: BaseHandler):
        pass

    def register_pipeline(self, pipeline: BasePipeline):
        self.__pipelines.append(pipeline)

    def register_notification(self, notification: BaseNotification, handlers: List[BaseNotificationHandler]):
        pass

    def get_requests(self):
        return self.__requests

    def get_notifications(self):
        return self.__notifications

    def get_pipelines(self):
        return self.__pipelines


class TestMediatrContainer(BaseTestCase):

    def setUp(self):
        pass

    def test_read_default_values_when_create_instance(self):
        # Given

        # When
        mediatr = Mediatr()

        # Then
        assert mediatr.mediatr_container is None

    def test_ready_when_is_ready(self):
        # Given
        mediatr = Mediatr()
        mediatr.is_ready = True

        # When
        mediatr.ready({})

        # Then
        assert mediatr.mediatr_container is None

    def test_ready_when_is_not_ready(self):
        # Given
        mediatr_container = FakeMediatrContainer()
        mediatr = Mediatr()

        # When
        mediatr.ready(mediatr_container)

        # Then
        assert mediatr.mediatr_container is mediatr_container
        assert mediatr.is_ready
        assert len(mediatr_container.get_pipelines()) == 1

    def test_send_raise_exception_when_container_is_none(self):
        # Given
        class TestRequest(BaseRequest):
            pass

        mediatr = Mediatr()

        # When
        with self.assertRaises(Exception) as context:
            self.async_loop(mediatr.send(TestRequest()))

        # Then
        assert 'mediatr_container_is_none' == context.exception.args[0]

    def test_send_raise_exception_when_container_pipelines_is_empty(self):
        # Given
        class TestRequest(BaseRequest):
            pass

        mediatr = Mediatr()
        mediatr.mediatr_container = FakeMediatrContainer()

        # When
        with self.assertRaises(Exception) as context:
            self.async_loop(mediatr.send(TestRequest()))

        # Then
        assert 'mediatr_container_has_not_contain_any_pipeline' == context.exception.args[0]

    @mock.patch("app.pydiator.mediatr.BusinessPipeline")
    def test_send_return_business_pipeline_result_when_container_pipelines_is_empty(self, mock_business_pipeline):
        async def business_handle():
            return True

        MagicMock.__await__ = lambda x: business_handle().__await__()
        mediatr_container = FakeMediatrContainer()

        class TestRequest(BaseRequest):
            pass

        mediatr = Mediatr()
        mediatr.ready(mediatr_container)

        # When
        response = self.async_loop(mediatr.send(TestRequest()))

        # Then
        assert response is True
