from opentracing.ext import tags
from pydiator_core.interfaces import BasePipeline, BaseRequest
from opentracing_instrumentation import get_current_span
from app.utils.tracer_config import tracer


class TracerPipeline(BasePipeline):

    async def handle(self, req: BaseRequest) -> object:
        span_tags = {
            tags.SPAN_KIND: tags.SPAN_KIND_RPC_SERVER,
            req.get_class_name(): req,
        }

        with tracer.start_active_span(
                req.get_class_name(),
                child_of=get_current_span(), tags=span_tags,
        ):
            response = await self.next().handle(req)
            return response
