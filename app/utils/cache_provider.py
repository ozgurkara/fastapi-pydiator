import redis
from pydiator_core.interfaces import BaseCacheProvider
from app.utils import config
from app.utils.config import REDIS_HOST, REDIS_PORT, REDIS_DB, REDIS_KEY_PREFIX


class CacheProvider(BaseCacheProvider):
    key_prefix = "pydiator"

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
            raise Exception('CacheProvider:client is None')

        return self.client


def get_cache_provider():
    if config.DISTRIBUTED_CACHE_IS_ENABLED:
        client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
        return CacheProvider(client=client, key_prefix=REDIS_KEY_PREFIX)
    return None
