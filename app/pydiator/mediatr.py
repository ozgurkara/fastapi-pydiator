from app.pydiator.interfaces import BaseRequest, BaseNotification, BaseMediatr
from app.pydiator.default_pipeline import DefaultPipeline
from app.pydiator.mediatr_container import BaseMediatrContainer


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
        if len(pipelines) == 0:
            raise Exception("mediatr_container_has_not_contain_any_pipeline")

        return await pipelines[0].handle(req)

    async def publish(self, notification: BaseNotification, throw_exception: bool = False):
        notifications_obj = self.mediatr_container.get_notifications()
        if type(notification).__name__ not in notifications_obj:
            raise Exception("mediatr_container_has_not_contain_any_notification_handler")

        handlers = notifications_obj[type(notification).__name__]
        for h in handlers:
            if not throw_exception:
                try:
                    await h.handle(notification)
                except Exception as e:
                    print("exception_when_notification_handle:", str(e))
            else:
                await h.handle(notification)


pydiator = Mediatr()
