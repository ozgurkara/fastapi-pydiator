from unittest import mock

from app.data.todo.handlers.add_todo_data_handler import AddTodoDataHandler, AddTodoDataRequest, AddTodoDataResponse
from app.pydiator.mediatr import pydiator
from app.pydiator.mediatr_container import MediatrContainer
from tests.base_test_case import BaseTestCase


class TestAddTodoDataHandler(BaseTestCase):
    @mock.patch("app.data.todo.handlers.add_todo_data_handler.fake_todo_db")
    def test_handler_return_success(self, mock_fake_todo_db):
        # Given
        container = MediatrContainer()
        container.register_request(AddTodoDataRequest(), AddTodoDataHandler())
        pydiator.set_container(container)

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
