from typing import List
from types import FunctionType
from pydiator_core.interfaces import BaseRequest, BaseHandler, BasePipeline, BaseNotification, BaseNotificationHandler, \
    BaseMediatrContainer


class MediatrContainer(BaseMediatrContainer):

    def __init__(self):
        self.__requests = {}
        self.__notifications = {}
        self.__pipelines = []
        self.__base_request_get_class_method_name = BaseRequest.get_class_name.__name__
        self.__base_notification_get_class_method_name = BaseNotification.get_class_name.__name__

    def register_request(self, req: type, handler: BaseHandler):
        if not isinstance(handler, FunctionType) and not issubclass(handler, BaseHandler):
            return

        if hasattr(req, self.__base_request_get_class_method_name) and callable(
                getattr(req, self.__base_request_get_class_method_name)):
            req_type = getattr(req, self.__base_request_get_class_method_name)()
            self.__requests[req_type] = handler

    def register_pipeline(self, pipeline: BasePipeline):
        self.__pipelines.append(pipeline)

    def register_notification(self, notification: type, handlers: List[BaseNotificationHandler]):
        if hasattr(notification, self.__base_notification_get_class_method_name) and callable(
                getattr(notification, self.__base_notification_get_class_method_name)):
            notification_type = getattr(notification, self.__base_notification_get_class_method_name)()
            self.__notifications[notification_type] = handlers

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
