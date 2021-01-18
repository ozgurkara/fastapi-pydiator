import logging

from pydiator_core.interfaces import BaseNotificationHandler
from app.notification.todo_transaction.transaction_notification import TodoTransactionNotification


class TransactionLogSubscriber(BaseNotificationHandler):
    def __init__(self):
        pass

    async def handle(self, notification: TodoTransactionNotification):
        logging.info(f'the transaction completed. its id {notification.id}')
