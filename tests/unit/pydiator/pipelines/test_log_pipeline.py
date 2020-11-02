from unittest import mock
from unittest.mock import MagicMock

from app.pydiator.pipelines.log_pipeline import LogPipeline
from tests.base_test_case import BaseTestCase, TestRequest, TestResponse


class TestLogPipeline(BaseTestCase):
    def setUp(self):
        pass

    def test_handle_return_exception_when_next_is_none(self):
        # Given
        log_pipeline = LogPipeline()

        # When
        with self.assertRaises(Exception) as context:
            self.async_loop(log_pipeline.handle(TestRequest()))

        # Then
        assert context.exception.args[0] == 'pydiator_log_pipeline_next_error'

    def test_handle_when_response_is_str(self):
        # Given
        next_response_text = "next_response"

        async def next_handle(req):
            return next_response_text

        mock_test_pipeline = MagicMock()
        mock_test_pipeline.handle = next_handle

        log_pipeline = LogPipeline()
        log_pipeline.set_next(mock_test_pipeline)

        # When
        response = self.async_loop(log_pipeline.handle(TestRequest()))

        # Then
        assert response is not None
        assert response == next_response_text

    @mock.patch("app.pydiator.pipelines.log_pipeline.Serializer")
    def test_handle_when_response_is_instance_of_dict(self, mock_serializer):
        # Given
        next_response = TestResponse(success=True)

        async def next_handle(req):
            return next_response

        mock_test_pipeline = MagicMock()
        mock_test_pipeline.handle = next_handle

        log_pipeline = LogPipeline()
        log_pipeline.set_next(mock_test_pipeline)

        # When
        response = self.async_loop(log_pipeline.handle(TestRequest()))

        # Then
        assert response is not None
        assert response == next_response
        assert mock_serializer.deserialize.called
        assert mock_serializer.deserialize.call_count == 2

    @mock.patch("app.pydiator.pipelines.log_pipeline.Serializer")
    def test_handle_when_response_type_is_list(self, mock_serializer):
        # Given
        next_response = [TestResponse(success=True)]

        async def next_handle(req):
            return next_response

        mock_test_pipeline = MagicMock()
        mock_test_pipeline.handle = next_handle

        log_pipeline = LogPipeline()
        log_pipeline.set_next(mock_test_pipeline)

        # When
        response = self.async_loop(log_pipeline.handle(TestRequest()))

        # Then
        assert response is not None
        assert response == next_response
        assert len(response) == 1
        assert mock_serializer.deserialize.called
        assert mock_serializer.deserialize.call_count == 2
