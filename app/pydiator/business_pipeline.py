from app.pydiator.interfaces import BaseRequest, BasePipeline
from app.pydiator.mediatr_container import BaseMediatrContainer


class BusinessPipeline(BasePipeline):
    def __init__(self, mediatr_container: BaseMediatrContainer):
        self.mediatr_container = mediatr_container

    async def handle(self, req: BaseRequest) -> object:
        print("BusinessPipeline:handle")
        handler = self.mediatr_container.get_requests().get(type(req).__name__, None)
        if handler is None:
            raise Exception("handler_not_found")

        handle_func = getattr(handler, "handle", None)
        if not callable(handle_func):
            raise Exception("handle_function_has_not_found_in_handler")

        return await handler.handle(req)
