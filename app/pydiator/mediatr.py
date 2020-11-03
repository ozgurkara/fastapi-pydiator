from abc import ABC, abstractmethod
from app.pydiator.interfaces import BaseRequest, BaseNotification
from app.pydiator.default_pipeline import DefaultPipeline
from app.pydiator.mediatr_container import BaseMediatrContainer


class BaseMediatr(ABC):

    @abstractmethod
    async def send(self, req: BaseRequest) -> object:
        pass

    @abstractmethod
    async def publish(self, notification: BaseNotification, throw_exception: bool = False):
        pass


class Mediatr(BaseMediatr):

    def __init__(self):
        self.mediatr_container = None
        self.is_ready = False

    def ready(self, mediatr_container: BaseMediatrContainer):
        if self.is_ready:
            return

        self.mediatr_container = mediatr_container
        self.mediatr_container.prepare_pipes(DefaultPipeline(self.mediatr_container))
        self.is_ready = True

    async def send(self, req: BaseRequest) -> object:
        if self.mediatr_container is None:
            raise Exception("mediatr_container_is_none")

        pipelines = self.mediatr_container.get_pipelines()
        if 0 == len(pipelines):
            raise Exception("mediatr_container_has_not_contain_any_pipeline")

        return await pipelines[0].handle(req)

    async def publish(self, notification: BaseNotification, throw_exception: bool = False):
        handlers = self.mediatr_container.get_notifications()[type(notification).__name__]
        if len(handlers) == 0:
            return

        for h in handlers:
            if throw_exception:
                try:
                    await h.handle(notification)
                except Exception as e:
                    print("Oops!", str(e), "occured.")
            else:
                await h.handle(notification)


pydiator = Mediatr()
