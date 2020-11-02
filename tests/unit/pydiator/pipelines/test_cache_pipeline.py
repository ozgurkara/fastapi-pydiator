from unittest.mock import MagicMock

from app.pydiator.interfaces import CacheType
from app.pydiator.pipelines.cache_pipeline import CachePipeline
from tests.base_test_case import BaseTestCase, TestRequest, TestPipeline, TestRequestWithCacheable, TestResponse
from app.utils.serializer_helper import Serializer


class TestCachePipeline(BaseTestCase):
    def setUp(self):
        pass

    def test_handle_return_exception_when_next_is_none(self):
        # Given
        cache_pipeline = CachePipeline(None)

        # When
        with self.assertRaises(Exception) as context:
            self.async_loop(cache_pipeline.handle(TestRequest()))

        # Then
        assert context.exception.args[0] == 'pydiator_cache_pipeline_next_error'

    def test_handle_when_req_is_no_cache(self):
        # Given
        next_response = TestResponse(success=True)

        async def next_handle(req):
            return next_response

        cache_pipeline = CachePipeline(None)
        mock_test_pipeline = MagicMock()
        mock_test_pipeline.handle = next_handle
        cache_pipeline.set_next(mock_test_pipeline)

        test_request = TestRequestWithCacheable("cache_key", 1, CacheType.DISTRIBUTED)
        test_request.set_no_cache()

        # When
        response = self.async_loop(cache_pipeline.handle(test_request))

        # Then
        assert response is not None
        assert response == next_response

    def test_handle_when_req_cache_key_is_none(self):
        # Given
        next_response = TestResponse(success=True)

        async def next_handle(req):
            return next_response

        cache_pipeline = CachePipeline(None)
        mock_test_pipeline = MagicMock()
        mock_test_pipeline.handle = next_handle
        cache_pipeline.set_next(mock_test_pipeline)
        test_request = TestRequestWithCacheable(None, 1, CacheType.DISTRIBUTED)

        # When
        response = self.async_loop(cache_pipeline.handle(test_request))

        # Then
        assert response is not None
        assert response == next_response

    def test_handle_when_req_cache_key_is_empty(self):
        # Given
        next_response = TestResponse(success=True)

        async def next_handle(req):
            return next_response

        mock_test_pipeline = MagicMock()
        mock_test_pipeline.handle = next_handle

        cache_pipeline = CachePipeline(None)
        cache_pipeline.set_next(mock_test_pipeline)

        # When
        response = self.async_loop(cache_pipeline.handle(TestRequestWithCacheable("", 1, CacheType.DISTRIBUTED)))

        # Then
        assert response is not None
        assert response == next_response

    def test_handle_when_req_result_is_not_in_cache(self):
        # Given
        next_response = TestResponse(success=True)

        async def next_handle(req):
            return next_response

        mock_test_pipeline = MagicMock()
        mock_test_pipeline.handle = next_handle

        mock_cache_provider = MagicMock()
        mock_cache_provider.get.return_value = None

        cache_pipeline = CachePipeline(mock_cache_provider)
        cache_pipeline.set_next(mock_test_pipeline)

        test_request = TestRequestWithCacheable("cache_key", 1, CacheType.DISTRIBUTED)

        # When
        response = self.async_loop(cache_pipeline.handle(test_request))

        # Then
        assert response is not None
        assert isinstance(response, TestResponse)
        assert response == next_response
        mock_cache_provider.get.assert_called_once_with(test_request.get_cache_key())
        mock_cache_provider.add.assert_called_once_with(test_request.get_cache_key(), Serializer.dumps(next_response),
                                                        test_request.get_cache_duration())

    def test_handle_when_req_result_is_in_cache(self):
        # Given
        next_response = TestResponse(success=True)

        mock_cache_provider = MagicMock()
        mock_cache_provider.get.return_value = Serializer.dumps(next_response)

        cache_pipeline = CachePipeline(mock_cache_provider)
        cache_pipeline.set_next(TestPipeline(True))

        # When
        response = self.async_loop(
            cache_pipeline.handle(TestRequestWithCacheable("cache_key", 1, CacheType.DISTRIBUTED)))

        # Then
        assert response is not None
        assert mock_cache_provider.get.call_count == 1

    def test_handle_when_req_is_not_instance_base_cacheable(self):
        # Given
        next_response = TestResponse(success=True)

        async def next_handle(req):
            return next_response

        mock_test_pipeline = MagicMock()
        mock_test_pipeline.handle = next_handle

        cache_pipeline = CachePipeline(None)
        cache_pipeline.set_next(mock_test_pipeline)

        # When
        response = self.async_loop(cache_pipeline.handle(TestRequest()))

        # Then
        assert response is not None
        assert response == next_response
