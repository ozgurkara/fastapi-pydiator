from pydiator_core.interfaces import BaseNotificationHandler

from app.notification.todo_transaction.transaction_notification import TodoTransactionNotification
from app.utils.cache_provider import get_cache_provider


class TransactionLogSubscriber(BaseNotificationHandler):
    def __init__(self):
        self.cache_provider = get_cache_provider()

    async def handle(self, notification: TodoTransactionNotification):
        print(f'the transaction completed. its id {notification.id}')
