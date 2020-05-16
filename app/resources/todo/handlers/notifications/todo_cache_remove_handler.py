from pydantic import BaseModel
from app.utils.client_factory import get_redis_client
from app.pydiator.interfaces import BaseNotification, BaseNotificationHandler
from app.utils.distributed_cache_provider import DistributedCacheProvider
from app.resources.todo.handlers.get_todo_all_handler import GetTodoAllRequest


class TodoChangeNotification(BaseModel, BaseNotification):
    pass


class TodoCacheRemoveNotificationHandler(BaseNotificationHandler):
    def __init__(self):
        self.cache_provider = DistributedCacheProvider(get_redis_client())

    async def handle(self, notification: BaseNotification):
        self.cache_provider.delete(GetTodoAllRequest().get_cache_key())
