from typing import List
from app.pydiator.interfaces import BaseRequest, BasePipeline
from app.utils.serializer_helper import Serializer


class LogPipeline(BasePipeline):
    async def handle(self, req: BaseRequest) -> object:
        print(f"LogPipeline:handle:{type(req).__name__}")

        if self.next() is None:
            raise Exception("pydiator_log_pipeline_next_error")

        response = await self.next().handle(req)

        if hasattr(response, "__dict__") or isinstance(response, List):
            _response = Serializer.deserialize(response)
        else:
            _response = str(response)

        log_obj = {
            "req": Serializer.deserialize(req),
            "res": _response
        }

        print("log", log_obj)

        return response
