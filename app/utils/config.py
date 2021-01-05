from starlette.config import Config

from dotenv import load_dotenv

load_dotenv()
config = Config(".env")

redis_host = config('RedisHost', str, '0.0.0.0')
redis_port = config('RedisPort', int, 6379)
redis_db = config('RedisDb', int, 0)
redis_key_prefix = config('RedisKeyPrefix', str, 'pydiator_api:')

distributed_cache_is_active = config("DistributedCacheIsActive", bool, False)
cache_pipeline_is_active = config("CachePipelineIsActive", bool, True)

jaeger_host = config('JaegerHost', str, '0.0.0.0')
jaeger_port = config('JaegerPort', int, 5775)
jaeger_sampler_type = config('JaegerSamplerType', str, 'probabilistic')
jaeger_sampler_rate = config('JaegerSamplerRate', float, 1.0)
jaeger_trace_id_header = config('JaegerTraceIdHeader', str, 'Trace-Id')
jaeger_service_name = config('JaegerServiceName', str, 'fastapi-pydiator')
