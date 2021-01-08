from jaeger_client import Config
from opentracing.scope_managers.asyncio import AsyncioScopeManager

from app.utils.config import JAEGER_HOST, JAEGER_PORT, JAEGER_SAMPLER_RATE, JAEGER_SAMPLER_TYPE, JAEGER_TRACE_ID_HEADER, \
    JAEGER_SERVICE_NAME


def init_tracer(service_name: str):
    config = Config(
        config={
            "local_agent": {
                "reporting_host": JAEGER_HOST,
                "reporting_port": JAEGER_PORT,
            },
            "sampler": {
                "type": JAEGER_SAMPLER_TYPE,
                "param": JAEGER_SAMPLER_RATE
            },
            "trace_id_header": JAEGER_TRACE_ID_HEADER,
        },
        scope_manager=AsyncioScopeManager(),
        service_name=service_name,
        validate=True,
    )
    return config.initialize_tracer()


tracer = init_tracer(JAEGER_SERVICE_NAME)
