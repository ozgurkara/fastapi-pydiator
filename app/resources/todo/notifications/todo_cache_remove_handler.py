from pydantic import BaseModel
from app.utils.client_factory import get_distributed_cache_provider
from pydiator_core.interfaces import BaseNotification, BaseNotificationHandler
from app.resources.todo.usecases.get_todo_all import GetTodoAllRequest


class TodoChangePublisherRequest(BaseModel, BaseNotification):
    pass


class TodoCacheRemoveSubscriber(BaseNotificationHandler):
    def __init__(self):
        self.cache_provider = get_distributed_cache_provider()

    async def handle(self, notification: BaseNotification):
        self.cache_provider.delete(GetTodoAllRequest().get_cache_key())
