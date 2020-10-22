from app.pydiator.interfaces import BaseRequest, BasePipeline, BaseCacheable, CacheType
from app.utils.distributed_cache_provider import BaseCacheProvider
from app.utils.serializer_helper import Serializer


class CachePipeline(BasePipeline):
    def __init__(self, cache_provider: BaseCacheProvider) -> None:
        self.cache_provider = cache_provider

    async def handle(self, req: BaseRequest) -> object:
        print("CachePipeline:handle")

        if self.next() is None:
            raise Exception("pydiator_cache_pipeline_next_error")

        response = None

        if isinstance(req, BaseCacheable):
            cache_type = req.get_cache_type()
            cache_key = req.get_cache_key()
            cache_duration = req.get_cache_duration()
            no_cache = req.is_no_cache()

            if cache_type == CacheType.DISTRIBUTED:
                cached_obj = self.get_from_cache(cache_key, no_cache)
                if cached_obj is not None:
                    return cached_obj

            response = await self.next().handle(req)
            if response is not None or response != "":
                self.add_to_cache(response, cache_key, cache_duration, no_cache)

        if response is None:
            response = await self.next().handle(req)

        return response

    def get_from_cache(self, cache_key, no_cache) -> object:
        if cache_key is not None and no_cache is False:
            cached_obj_str = self.cache_provider.get(cache_key)
            if cached_obj_str is not None:
                return Serializer.loads(cached_obj_str)

        return None

    def add_to_cache(self, res: object, cache_key, cache_duration, no_cache):
        if res is not None and cache_key is not None and cache_duration > 0 and no_cache is False:
            res_value_obj = Serializer.dumps(res)
            if res_value_obj is not None:
                self.cache_provider.add(cache_key, res_value_obj, cache_duration)
