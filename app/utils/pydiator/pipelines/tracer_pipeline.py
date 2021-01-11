from app.utils.tracer_config import tracer
from pydiator_core.interfaces import BasePipeline, BaseRequest
from opentracing.ext import tags
from opentracing_instrumentation import get_current_span

from fastapi_contrib.tracing.middlewares import request_span


class TracerPipeline(BasePipeline):

    async def handle(self, req: BaseRequest, **kwargs) -> object:
        current_span = get_current_span()
        if get_current_span() is None:
            current_span = request_span.get()

        span_tags = {
            tags.SPAN_KIND: tags.SPAN_KIND_RPC_SERVER,
            "request_type": req.get_class_name(),
            "request_value": req
        }

        with tracer.start_active_span(req.get_class_name(), child_of=current_span, tags=span_tags,
                                      finish_on_close=True):
            response = await self.next().handle(req=req, **kwargs)
            return response
