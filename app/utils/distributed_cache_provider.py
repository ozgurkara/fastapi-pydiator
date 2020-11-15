from abc import ABC, abstractmethod
from pydiator_core.interfaces import BaseCacheProvider


class DistributedCacheProvider(BaseCacheProvider):
    key_prefix = None

    def __init__(self, client):
        self.client = client
        if self.key_prefix is None:
            self.key_prefix = "default_prefix"

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
        return '{}:{}'.format(self.key_prefix, key)

    def __get_client(self):
        if self.client is None:
            raise Exception('env:RedisHost is None')

        return self.client


class FakeDistributedCacheProvider(BaseCacheProvider):
    def __init__(self):
        pass

    def add(self, key: str, value, expires):
        pass

    def get(self, key: str):
        pass

    def exist(self, key: str):
        pass

    def delete(self, key: str):
        pass

    def check_connection(self):
        pass
