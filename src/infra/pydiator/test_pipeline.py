import inspect
from types import FunctionType
from pydiator_core.interfaces import BaseRequest, BasePipeline, BaseHandler
from pydiator_core.mediatr_container import BaseMediatrContainer


class TestPipeline(BasePipeline):
    def __init__(self, mediatr_container: BaseMediatrContainer):
        self.mediatr_container = mediatr_container

    async def handle(self, req: BaseRequest, **kwargs) -> object:
        req_type_name = req.get_class_name()

        handler_source = self.mediatr_container.get_requests().get(req_type_name, None)
        if handler_source is None:
            raise Exception(f"handler_not_found_for_request_:{req_type_name}")

        handler_instance = handler_source()
        handler_handle_func = getattr(handler_instance, "handle", None)
        if not callable(handler_handle_func):
            raise Exception("handle_function_has_not_found_in_handler")

        is_async = inspect.iscoroutinefunction(handler_instance.handle)
        if not is_async:
            return handler_instance.handle(req)

        return await handler_instance.handle(req)
