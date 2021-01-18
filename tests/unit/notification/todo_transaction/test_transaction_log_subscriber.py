from unittest import mock
from app.notification.todo_transaction.transaction_log_subscriber import TransactionLogSubscriber
from app.notification.todo_transaction.transaction_notification import TodoTransactionNotification
from tests.unit.base_test_case import BaseTestCase


class TestTransactionLogSubscriber(BaseTestCase):

    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    @mock.patch("app.notification.todo_transaction.transaction_log_subscriber.logging")
    def test_handle(self, mock_logging):
        # Given
        subscriber = TransactionLogSubscriber()
        notification = TodoTransactionNotification(id=1)

        # When
        self.async_loop(subscriber.handle(notification=notification))

        # Then
        assert mock_logging.info.called
        assert mock_logging.info.call_count == 1
        assert mock_logging.info.call_args.args[0] == f'the transaction completed. its id {notification.id}'
