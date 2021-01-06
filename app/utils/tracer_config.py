from jaeger_client import Config
from opentracing.scope_managers.asyncio import AsyncioScopeManager

from app.utils.config import jaeger_host, jaeger_port, jaeger_sampler_rate, jaeger_sampler_type, jaeger_trace_id_header, \
    jaeger_service_name


def init_tracer(service_name: str):
    config = Config(
        config={
            "enabled": False,
            "local_agent": {
                "reporting_host": jaeger_host,
                "reporting_port": jaeger_port,
            },
            "sampler": {
                "type": jaeger_sampler_type,
                "param": jaeger_sampler_rate
            },
            "trace_id_header": jaeger_trace_id_header,
            "logging": False
        },
        scope_manager=AsyncioScopeManager(),
        service_name=service_name,
        validate=True,
    )
    return config.initialize_tracer()


tracer = init_tracer(jaeger_service_name)
