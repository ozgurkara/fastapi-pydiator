import redis
from pydiator_core.interfaces import BaseCacheProvider
from app.utils import config
from app.utils.config import redis_host, redis_port, redis_db, redis_key_prefix


class DistributedCacheProvider(BaseCacheProvider):
    key_prefix = "default_prefix"

    def __init__(self, client, key_prefix: str = None):
        self.client = client
        self.key_prefix = key_prefix

    def add(self, key: str, value, expires):
        return self.__get_client().set(self.__get_formatted_key(key), value, ex=expires)

    def get(self, key):
        return self.__get_client().get(self.__get_formatted_key(key))

    def exist(self, key):
        return self.__get_client().exists(self.__get_formatted_key(key))

    def delete(self, key):
        self.__get_client().delete(self.__get_formatted_key(key))

    def check_connection(self):
        result = self.__get_client().echo("echo")
        if result == b'echo':
            return True
        return False

    def __get_formatted_key(self, key) -> str:
        return '{}:{}'.format(self.key_prefix, key)

    def __get_client(self):
        if self.client is None:
            raise Exception('DistributedCacheProvider:client is None')

        return self.client


def get_distributed_cache_provider():
    if config.distributed_cache_is_active:
        client = redis.Redis(host=redis_host, port=redis_port, db=redis_db)
        return DistributedCacheProvider(client=client, key_prefix=redis_key_prefix)
    return None
