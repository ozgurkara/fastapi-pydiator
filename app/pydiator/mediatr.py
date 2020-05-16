from abc import ABC, abstractmethod
from app.pydiator.interfaces import BaseRequest, BaseNotification
from app.pydiator.business_pipeline import BusinessPipeline
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

    def set_container(self, mediatr_container: BaseMediatrContainer):
        self.mediatr_container = mediatr_container

    async def send(self, req: BaseRequest) -> object:
        if self.mediatr_container is None:
            raise Exception("mediatr_container_is_none")

        business_pipeline = BusinessPipeline(self.mediatr_container)
        pipelines = self.mediatr_container.get_pipelines()
        if len(pipelines) > 0:
            main_pipeline = None
            for i in range(len(pipelines) - 1, -1, -1):
                if i == (len(pipelines) - 1):
                    pipeline = pipelines[i]
                    pipeline.set_next(business_pipeline)
                    main_pipeline = pipelines[i]
                else:
                    pipelines[i].set_next(main_pipeline)
                    main_pipeline = pipelines[i]

            if main_pipeline is not None:
                return await main_pipeline.handle(req)
            else:
                raise Exception("main_pipeline_is_none")

        else:
            return await business_pipeline.handle(req)

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
