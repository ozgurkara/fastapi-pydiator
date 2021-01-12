from unittest import mock

from app.data.todo.usecases.add_todo_data import AddTodoDataUseCase, AddTodoDataRequest, AddTodoDataResponse
from pydiator_core.mediatr import pydiator
from tests.unit.base_test_case import BaseTestCase


class TestAddTodoDataUseCase(BaseTestCase):
    def setUp(self):
        self.register_request(AddTodoDataRequest(), AddTodoDataUseCase())

    @mock.patch("app.data.todo.usecases.add_todo_data.fake_todo_db")
    def test_handle_return_success(self, mock_fake_todo_db):
        # Given
        self.register_request(AddTodoDataRequest(), AddTodoDataUseCase())
        mock_fake_todo_db.__iter__.return_value = []

        title_val = "title"
        request = AddTodoDataRequest(title=title_val)
        expected_response = AddTodoDataResponse(success=True, id=1)

        # When
        response = self.async_loop(pydiator.send(request))

        # Then
        assert response == expected_response
        assert mock_fake_todo_db.append.call_count == 1
        assert mock_fake_todo_db.append.called
