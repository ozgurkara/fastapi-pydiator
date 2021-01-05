from app.utils.tracer_config import tracer
from pydiator_core.interfaces import BasePipeline, BaseRequest
from opentracing.ext import tags
from opentracing_instrumentation import get_current_span

from fastapi_contrib.tracing.middlewares import request_span


class TracerPipeline(BasePipeline):

    async def handle(self, req: BaseRequest) -> object:
        current_span = get_current_span()
        if get_current_span() is None:
            try:
                current_span = request_span.get()
            except:
                pass

        span_tags = {
            tags.SPAN_KIND: tags.SPAN_KIND_RPC_SERVER,
            req.get_class_name(): req,
        }

        with tracer.start_active_span(req.get_class_name(), child_of=current_span, tags=span_tags):
            response = await self.next().handle(req)
            return response
