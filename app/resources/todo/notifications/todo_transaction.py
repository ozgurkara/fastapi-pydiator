from pydantic import BaseModel
from pydiator_core.interfaces import BaseNotification, BaseNotificationHandler
from app.resources.todo.usecases.get_todo_all import GetTodoAllRequest
from app.utils.distributed_cache_provider import get_distributed_cache_provider


class TodoTransactionPublisherRequest(BaseModel, BaseNotification):
    pass


class TodoCacheRemoveSubscriber(BaseNotificationHandler):
    def __init__(self):
        self.cache_provider = get_distributed_cache_provider()

    async def handle(self, notification: BaseNotification):
        self.cache_provider.delete(GetTodoAllRequest().get_cache_key())
