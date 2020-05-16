from abc import ABC, abstractmethod


class BaseCacheProvider(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def add(self, key: str, value, expires):
        pass

    @abstractmethod
    def get(self, key: str):
        pass

    @abstractmethod
    def exist(self, key: str):
        pass

    @abstractmethod
    def delete(self, key: str):
        pass

    @abstractmethod
    def check_connection(self):
        pass


class DistributedCacheProvider(BaseCacheProvider):
    redis_key_prefix = None

    def __init__(self, client):
        self.client = client
        if self.redis_key_prefix is None:
            self.redis_key_prefix = "default_prefix"

    def add(self, key: str, value, expires):
        return self.__get_client().set(self.__get_formatted_key(key), value, ex=expires)

    def get(self, key):
        return self.__get_client().get(self.__get_formatted_key(key))

    def exist(self, key):
        return self.__get_client().exists(self.__get_formatted_key(key))

    def delete(self, key):
        self.__get_client().delete(self.__get_formatted_key(key))

    def check_connection(self, ):
        result = self.__get_client().echo("echo")
        if result == b'echo':
            return True
        return False

    def __get_formatted_key(self, key) -> str:
        return '{}:{}'.format(self.redis_key_prefix, key)

    def __get_client(self):
        if self.client is None:
            raise Exception('env:RedisHost is None')

        return self.client

# distributed_cache_provider = RedisCacheProvider()
