from typing import List
from app.pydiator.interfaces import BaseRequest, BaseHandler, BasePipeline, BaseNotification, BaseNotificationHandler, \
    BaseMediatrContainer


class MediatrContainer(BaseMediatrContainer):

    def __init__(self):
        self.__requests = {}
        self.__notifications = {}
        self.__pipelines = []

    def register_request(self, req: BaseRequest, handler: BaseHandler):
        if not isinstance(req, BaseRequest) or not isinstance(handler, BaseHandler):
            return

        self.__requests[type(req).__name__] = handler

    def register_pipeline(self, pipeline: BasePipeline):
        self.__pipelines.append(pipeline)

    def register_notification(self, notification: BaseNotification, handlers: List[BaseNotificationHandler]):
        self.__notifications[type(notification).__name__] = handlers

    def get_requests(self):
        return self.__requests

    def get_notifications(self):
        return self.__notifications

    def get_pipelines(self):
        return self.__pipelines

    def prepare_pipes(self, pipeline: BasePipeline):
        self.register_pipeline(pipeline)
        pipelines_length = len(self.__pipelines)
        if pipelines_length == 1:
            return

        for i in range(pipelines_length - 1, -1, -1):
            if 0 == i:
                break
            self.__pipelines[i - 1].set_next(self.__pipelines[i])
