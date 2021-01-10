from unittest import mock

from pydiator_core.interfaces import BaseRequest, BasePipeline

from app.utils.pydiator.pipelines.tracer_pipeline import TracerPipeline
from tests.unit.base_test_case import BaseTestCase


class TestTracerPipeline(BaseTestCase):
    def setUp(self):
        pass

    def tearDown(self) -> None:
        pass

    @mock.patch("app.utils.pydiator.pipelines.tracer_pipeline.tracer")
    @mock.patch("app.utils.pydiator.pipelines.tracer_pipeline.request_span")
    @mock.patch("app.utils.pydiator.pipelines.tracer_pipeline.get_current_span")
    def test_current_span_is_none(self, mock_get_current_span, mock_request_span, mock_tracer):
        # Given
        mock_get_current_span.return_value = None
        mock_request_span.get.return_value = {}

        class Pipeline(BasePipeline):
            async def handle(self, req: BaseRequest) -> object:
                return None

        next_pipeline = Pipeline()
        pipeline = TracerPipeline()
        pipeline.set_next(next_pipeline)

        class TestRequest(BaseRequest):
            pass

        # When
        response = self.async_loop(pipeline.handle(req=TestRequest()))

        # Then
        assert response is None
        assert mock_tracer.start_active_span.called
        assert mock_tracer.start_active_span.call_count == 1
        assert mock_tracer.start_active_span.call_args.args[0] == TestRequest.get_class_name()
        assert mock_tracer.start_active_span.call_args.kwargs['child_of'] == {}

    @mock.patch("app.utils.pydiator.pipelines.tracer_pipeline.tracer")
    @mock.patch("app.utils.pydiator.pipelines.tracer_pipeline.get_current_span")
    def test_current_span_is_not_none(self, mock_get_current_span, mock_tracer):
        # Given
        mock_get_current_span.return_value = {}

        class Pipeline(BasePipeline):
            async def handle(self, req: BaseRequest) -> object:
                return None

        next_pipeline = Pipeline()
        pipeline = TracerPipeline()
        pipeline.set_next(next_pipeline)

        class TestRequest(BaseRequest):
            pass

        # When
        response = self.async_loop(pipeline.handle(req=TestRequest()))

        # Then
        assert response is None
        assert mock_tracer.start_active_span.called
        assert mock_tracer.start_active_span.call_count == 1
        assert mock_tracer.start_active_span.call_args.args[0] == TestRequest.get_class_name()
        assert mock_tracer.start_active_span.call_args.kwargs['child_of'] == {}
