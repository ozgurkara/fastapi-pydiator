from jaeger_client import Config
from opentracing.scope_managers.asyncio import AsyncioScopeManager

JAEGER_HOST = '0.0.0.0'
JAEGER_PORT = 5775
JAEGER_SAMPLER_TYPE = 'probabilistic'
JAEGER_SAMPLER_RATE = 1.0
JAEGER_TRACE_ID_HEADER = 'ss'
JAEGER_IP_TAG_KEY = 1


def init_tracer(service_name: str):
    print("init_tracer")
    config = Config(
        config={
            "local_agent": {
                "reporting_host": JAEGER_HOST,
                "reporting_port": JAEGER_PORT,
            },
            "sampler": {"type": JAEGER_SAMPLER_TYPE, "param": JAEGER_SAMPLER_RATE},
            "trace_id_header": JAEGER_TRACE_ID_HEADER,
            # "generate_128bit_trace_id": JAEGER_TRACEID_128BIT,
        },
        scope_manager=AsyncioScopeManager(),
        service_name=service_name,
        validate=True,
    )
    return config.initialize_tracer()


tracer = init_tracer("pydiator-api")
