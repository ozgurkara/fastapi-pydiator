from starlette.config import Config

from dotenv import load_dotenv

load_dotenv()
config = Config(".env")

REDIS_HOST = config('REDIS_HOST', str, '0.0.0.0')
REDIS_PORT = config('REDIS_PORT', int, 6379)
REDIS_DB = config('REDIS_DB', int, 0)
REDIS_KEY_PREFIX = config('REDIS_KEY_PREFIX', str, 'fastapi_pydiator:')

DISTRIBUTED_CACHE_IS_ENABLED = config("DISTRIBUTED_CACHE_IS_ENABLED", bool, True)
CACHE_PIPELINE_IS_ENABLED = config("CACHE_PIPELINE_IS_ENABLED", bool, True)
LOG_PIPELINE_IS_ENABLED = config("LOG_PIPELINE_IS_ENABLED", bool, True)
TRACER_PIPELINE_IS_ENABLED = config("TRACER_PIPELINE_IS_ENABLED", bool, True)
TRACER_IS_ENABLED = config('TRACER_IS_ENABLED', bool, True)

JAEGER_HOST = config('JAEGER_HOST', str, '0.0.0.0')
JAEGER_PORT = config('JAEGER_PORT', int, 5775)
JAEGER_SAMPLER_TYPE = config('JAEGER_SAMPLER_TYPE', str, 'probabilistic')
JAEGER_SAMPLER_RATE = config('JAEGER_SAMPLER_RATE', float, 1.0)
JAEGER_TRACE_ID_HEADER = config('JAEGER_TRACE_ID_HEADER', str, 'x-trace-id')
JAEGER_SERVICE_NAME = config('JAEGER_SERVICE_NAME', str, 'fastapi_pydiator')
