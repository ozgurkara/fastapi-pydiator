from unittest import mock

from app.pydiator.mediatr import Mediatr
from tests.base_test_case import BaseTestCase, TestRequest, TestResponse, FakeMediatrContainer


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
        mediatr = Mediatr()

        # When
        with self.assertRaises(Exception) as context:
            self.async_loop(mediatr.send(TestRequest()))

        # Then
        assert 'mediatr_container_is_none' == context.exception.args[0]

    def test_send_raise_exception_when_container_pipelines_is_empty(self):
        # Given
        mediatr = Mediatr()
        mediatr.mediatr_container = FakeMediatrContainer()

        # When
        with self.assertRaises(Exception) as context:
            self.async_loop(mediatr.send(TestRequest()))

        # Then
        assert 'mediatr_container_has_not_contain_any_pipeline' == context.exception.args[0]

    @mock.patch("app.pydiator.mediatr.DefaultPipeline")
    def test_send_return_default_pipeline_result_when_container_pipelines_is_empty(self, mock_business_pipeline):
        # Given
        next_response = TestResponse(success=True)

        async def next_handle(req):
            return next_response

        mock_business_pipeline.return_value.handle = next_handle
        mediatr_container = FakeMediatrContainer()
        mediatr = Mediatr()
        mediatr.ready(mediatr_container)

        # When
        response = self.async_loop(mediatr.send(TestRequest()))

        # Then
        assert response is next_response
        assert response.success
