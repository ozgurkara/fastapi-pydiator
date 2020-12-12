from unittest import mock

from app.data.todo.usecases.get_todo_by_id_data import GetTodoByIdDataResponse
from pydiator_core.mediatr import pydiator
from app.resources.todo.usecases.get_todo_by_id import \
    GetTodoByIdRequest, GetTodoByIdResponse, GetTodoByIdUseCase
from tests.base_test_case import BaseTestCase


class TestGetTodoByIdHandler(BaseTestCase):
    def setUp(self):
        self.register_request(GetTodoByIdRequest(), GetTodoByIdUseCase())

    @mock.patch("app.resources.todo.usecases.get_todo_by_id.pydiator")
    def test_handler_return_todo(self, mock_pydiator):
        # Given
        id_val = 1
        title_val = "title 1"
        mock_pydiator.send.side_effect = [self.async_return(GetTodoByIdDataResponse(id=id_val, title=title_val))]

        request = GetTodoByIdRequest(id=id_val)
        expected_response = GetTodoByIdResponse(id=id_val, title=title_val)

        # When
        response = self.async_loop(pydiator.send(request))

        # Then
        assert response == expected_response

    @mock.patch("app.resources.todo.usecases.get_todo_by_id.pydiator")
    def test_handler_return_none(self, mock_pydiator):
        # Given
        mock_pydiator.send.side_effect = [self.async_return(None)]
        request = GetTodoByIdRequest(id=1)
        expected_response = None

        # When
        response = self.async_loop(pydiator.send(request))

        # Then
        assert response == expected_response
