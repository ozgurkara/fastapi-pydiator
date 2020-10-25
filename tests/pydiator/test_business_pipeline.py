from unittest import mock

from app.pydiator.business_pipeline import BusinessPipeline
from app.pydiator.interfaces import BaseRequest, BaseResponse, BaseHandler
from app.pydiator.mediatr_container import MediatrContainer
from tests.base_test_case import BaseTestCase


class TestBusinessPipeline(BaseTestCase):
    def setUp(self):
        pass

    def test_handle_return_exception_when_handler_is_not(self):
        # Given
        pipeline = BusinessPipeline(MediatrContainer())

        class TestRequest(BaseRequest):
            pass

        # When

        # Then
        with self.assertRaises(Exception) as context:
            self.async_loop(pipeline.handle(req=TestRequest()))

        assert 'handler_not_found' == context.exception.args[0]

    def test_handle_return_exception_when_handler_is_not_callable(self):
        # Given

        class TestRequest(BaseRequest):
            pass

        mock_container = mock.MagicMock()
        mock_container.get_requests.return_value.get.return_value = {}
        self.pipeline = BusinessPipeline(mock_container)

        # When
        with self.assertRaises(Exception) as context:
            self.async_loop(self.pipeline.handle(req=TestRequest()))

        # Then
        assert 'handle_function_has_not_found_in_handler' == context.exception.args[0]

    def test_handle_return_handle_response(self):
        # Given
        class TestRequest(BaseRequest):
            pass

        class TestResponse(BaseResponse):
            pass

        class TestHandler(BaseHandler):
            async def handle(self, req: BaseRequest):
                return TestResponse()

        container = MediatrContainer()
        container.register_request(TestRequest(), TestHandler())
        self.pipeline = BusinessPipeline(container)

        # When
        response = self.async_loop(self.pipeline.handle(req=TestRequest()))

        # Then
        assert isinstance(response, BaseResponse)
        assert isinstance(response, TestResponse)
