import os

redis_host = os.getenv('RedisHost', '0.0.0.0')
redis_port = int(os.getenv('RedisPort', 6379))
redis_db = int(os.getenv('RedisDb', 0))
redis_key_prefix = os.getenv('RedisKeyPrefix', 'pydiator_api:')

distributed_cache_is_active = bool(os.environ.get("DistributedCacheIsActive", True))
cache_pipeline_is_active = bool(os.environ.get("CachePipelineIsActive", True))
