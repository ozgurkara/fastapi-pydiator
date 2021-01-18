from pydiator_core.interfaces import BaseNotificationHandler

from app.notification.todo_transaction.transaction_notification import TodoTransactionNotification
from app.resources.todo.usecases.get_todo_all import GetTodoAllRequest
from app.utils.cache_provider import get_cache_provider


class TodoRemoveCacheSubscriber(BaseNotificationHandler):
    def __init__(self):
        self.cache_provider = get_cache_provider()

    async def handle(self, notification: TodoTransactionNotification):
        self.cache_provider.delete(GetTodoAllRequest().get_cache_key())
