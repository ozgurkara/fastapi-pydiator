from unittest import mock

from app.data.todo.handlers.add_todo_data_handler import AddTodoDataHandler, AddTodoDataRequest, AddTodoDataResponse
from app.pydiator.mediatr import pydiator
from tests.base_test_case import BaseTestCase


class TestAddTodoDataHandler(BaseTestCase):
    def setUp(self):
        self.register_request(AddTodoDataRequest(), AddTodoDataHandler())

    @mock.patch("app.data.todo.handlers.add_todo_data_handler.fake_todo_db")
    def test_handler_return_success(self, mock_fake_todo_db):
        # Given
        self.register_request(AddTodoDataRequest(), AddTodoDataHandler())
        mock_fake_todo_db.__iter__.return_value = []

        title_val = "title"
        request = AddTodoDataRequest(title=title_val)
        expected_response = AddTodoDataResponse(success=True)

        # When
        response = self.async_loop(pydiator.send(request))

        # Then
        assert response == expected_response
        assert mock_fake_todo_db.append.call_count == 1
        assert mock_fake_todo_db.append.called
