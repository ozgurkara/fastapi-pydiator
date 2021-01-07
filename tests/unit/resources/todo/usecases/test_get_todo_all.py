from unittest import mock

from app.data.todo.usecases.get_todo_all_data import GetTodoAllDataResponse
from pydiator_core.mediatr import pydiator
from app.resources.todo.usecases.get_todo_all import GetTodoAllRequest, GetTodoAllUseCase, GetTodoAllResponse
from tests.unit.base_test_case import BaseTestCase


class TestGetTodoByIdUseCase(BaseTestCase):
    def setUp(self):
        self.register_request(GetTodoAllRequest, GetTodoAllUseCase())

    def tearDown(self):
        pass

    @mock.patch("app.resources.todo.usecases.get_todo_all.pydiator")
    def test_handle_return_list(self, mock_pydiator):
        # Given
        id_val = 1
        title_val = "title 1"
        mock_pydiator.send.side_effect = [self.async_return([GetTodoAllDataResponse(id=id_val, title=title_val)])]

        request = GetTodoAllRequest(id=id_val)
        expected_response = [GetTodoAllResponse(id=id_val, title=title_val)]

        # When
        response = self.async_loop(pydiator.send(request))

        # Then
        assert response is not None
        assert expected_response == response

    @mock.patch("app.resources.todo.usecases.get_todo_all.pydiator")
    def test_handle_return_empty_list(self, mock_pydiator):
        # Given
        mock_pydiator.send.side_effect = [self.async_return([])]
        request = GetTodoAllRequest(id=1)
        expected_response = []

        # When
        response = self.async_loop(pydiator.send(request))

        # Then
        assert response == expected_response
