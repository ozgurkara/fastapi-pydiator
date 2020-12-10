from unittest import mock

from app.data.todo.handlers.get_todo_all_data_handler import GetTodoAllDataResponse
from pydiator_core.mediatr import pydiator
from app.resources.todo.handlers.get_todo_all_handler import GetTodoAllRequest, GetTodoAllHandler, GetTodoAllResponse
from tests.base_test_case import BaseTestCase


class TestGetTodoByIdHandler(BaseTestCase):
    def setUp(self):
        self.register_request(GetTodoAllRequest(), GetTodoAllHandler())

    @mock.patch("app.resources.todo.handlers.get_todo_all_handler.pydiator")
    def test_handler_return_list(self, mock_pydiator):
        # Given
        id_val = 1
        title_val = "title 1"
        mock_pydiator.send.side_effect = [self.async_return([GetTodoAllDataResponse(id=id_val, title=title_val)])]

        request = GetTodoAllRequest(id=id_val)
        expected_response = [GetTodoAllResponse(id=id_val, title=title_val)]

        # When
        response = self.async_loop(pydiator.send(request))

        # Then
        assert response == expected_response

    @mock.patch("app.resources.todo.handlers.get_todo_all_handler.pydiator")
    def test_handler_return_empty_list(self, mock_pydiator):
        # Given
        mock_pydiator.send.side_effect = [self.async_return([])]
        request = GetTodoAllRequest(id=1)
        expected_response = []

        # When
        response = self.async_loop(pydiator.send(request))

        # Then
        assert response == expected_response
