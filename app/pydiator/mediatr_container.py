from abc import ABC, abstractmethod
from typing import List
from app.pydiator.interfaces import BaseRequest, BaseHandler, BasePipeline, BaseNotification, BaseNotificationHandler


class BaseMediatrContainer(ABC):

    @abstractmethod
    def register_request(self, req: BaseRequest, handler: BaseHandler):
        pass

    @abstractmethod
    def register_pipeline(self, pipeline: BasePipeline):
        pass

    @abstractmethod
    def register_notification(self, notification: BaseNotification, handlers: List[BaseNotificationHandler]):
        pass

    @abstractmethod
    def get_requests(self):
        pass

    @abstractmethod
    def get_notifications(self):
        pass

    @abstractmethod
    def get_pipelines(self):
        pass


class MediatrContainer(BaseMediatrContainer):

    def __init__(self):
        self.__requests = {}
        self.__notifications = {}
        self.__pipelines = []

    def register_request(self, req: BaseRequest, handler: BaseHandler):
        if not isinstance(req, BaseRequest) and not isinstance(handler, BaseHandler):
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
