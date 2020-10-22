import redis

from app.utils import environment
from app.utils.distributed_cache_provider import DistributedCacheProvider, FakeDistributedCacheProvider
from app.utils.environment import redis_host, redis_port, redis_db


def get_redis_client():
    return redis.Redis(host=redis_host, port=redis_port, db=redis_db)


def get_distributed_cache_provider():
    if environment.distributed_cache_is_active:
        return DistributedCacheProvider(get_redis_client())
    return FakeDistributedCacheProvider()
