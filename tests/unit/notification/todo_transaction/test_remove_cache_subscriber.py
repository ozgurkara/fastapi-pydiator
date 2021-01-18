from unittest import mock

from app.notification.todo_transaction.remove_cache_subscriber import TodoRemoveCacheSubscriber
from app.notification.todo_transaction.transaction_notification import TodoTransactionNotification
from app.resources.todo.usecases.get_todo_all import GetTodoAllRequest
from tests.unit.base_test_case import BaseTestCase


class TestTodoRemoveCacheSubscriber(BaseTestCase):

    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    @mock.patch("app.notification.todo_transaction.remove_cache_subscriber.get_cache_provider")
    def test_handle(self, mock_get_cache_provider):
        # Given
        subscriber = TodoRemoveCacheSubscriber()
        notification = TodoTransactionNotification()

        # When
        self.async_loop(subscriber.handle(notification=notification))

        # Then
        assert mock_get_cache_provider.return_value.delete.called
        assert mock_get_cache_provider.return_value.delete.call_count == 1
        assert mock_get_cache_provider.return_value.delete.call_args.args[0] == GetTodoAllRequest().get_cache_key()
