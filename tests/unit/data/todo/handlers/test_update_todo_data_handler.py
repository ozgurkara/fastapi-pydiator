from unittest import mock

from app.data.todo.handlers.update_todo_data_handler import UpdateTodoDataHandler, UpdateTodoDataRequest, \
    UpdateTodoDataResponse
from app.pydiator.mediatr import pydiator
from tests.base_test_case import BaseTestCase


class TestAddTodoHandler(BaseTestCase):
    def setUp(self):
        self.register_request(UpdateTodoDataRequest(), UpdateTodoDataHandler())

    @mock.patch("app.data.todo.handlers.update_todo_data_handler.fake_todo_db")
    def test_handler_return_success(self, mock_fake_todo_db):
        # Given
        id_val = 1
        mock_fake_todo_db.__iter__.return_value = [{"id": id_val, "title": "title 1"}]
        title_val = "title 1 updated"
        request = UpdateTodoDataRequest(title=title_val)
        request.id = id_val
        expected_response = UpdateTodoDataResponse(success=True)

        # When
        response = self.async_loop(pydiator.send(request))

        # Then
        assert response == expected_response

    @mock.patch("app.data.todo.handlers.update_todo_data_handler.fake_todo_db")
    def test_handler_return_fail(self, mock_fake_todo_db):
        # Given
        mock_fake_todo_db.__iter__.return_value = []
        title_val = "title 1 updated"
        request = UpdateTodoDataRequest(title=title_val)
        request.id = id
        expected_response = UpdateTodoDataResponse(success=False)

        # When
        response = self.async_loop(pydiator.send(request))

        # Then
        assert response == expected_response
