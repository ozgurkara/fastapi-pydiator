from pydiator_core.interfaces import BaseNotificationHandler

from src.notification.todo_transaction.transaction_notification import TodoTransactionNotification
from src.api.controller.todo.todo_controller import GetTodoAllRequest
from src.infra.pydiator.cache_provider import get_cache_provider


class TodoRemoveCacheSubscriber(BaseNotificationHandler):
    def __init__(self):
        self.cache_provider = get_cache_provider()

    async def handle(self, notification: TodoTransactionNotification):
        self.cache_provider.delete(GetTodoAllRequest().get_cache_key())
