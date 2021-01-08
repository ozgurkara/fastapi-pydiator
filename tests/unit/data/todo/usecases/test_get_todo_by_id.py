from unittest import mock

from app.data.todo.usecases.get_todo_by_id_data import GetTodoByIdDataUseCase, GetTodoByIdDataRequest, \
    GetTodoByIdDataResponse
from pydiator_core.mediatr import pydiator
from tests.unit.base_test_case import BaseTestCase


class TestGetTodoByIdDataUseCase(BaseTestCase):
    def setUp(self):
        self.register_request(GetTodoByIdDataRequest(), GetTodoByIdDataUseCase())

    @mock.patch("app.data.todo.usecases.get_todo_by_id_data.fake_todo_db")
    def test_handle_return_todo(self, mock_fake_todo_db):
        # Given
        id_val = 1
        title_val = "title 1"
        mock_fake_todo_db.__iter__.return_value = [{"id": id_val, "title": title_val}]

        request = GetTodoByIdDataRequest(id=id_val)
        expected_response = GetTodoByIdDataResponse(id=id_val, title=title_val)

        # When
        response = self.async_loop(pydiator.send(request))

        # Then
        assert response == expected_response

    @mock.patch("app.data.todo.usecases.get_todo_by_id_data.fake_todo_db")
    def test_handle_return_none_when_todo_is_not_exist(self, mock_fake_todo_db):
        # Given
        mock_fake_todo_db.__iter__.return_value = []
        request = GetTodoByIdDataRequest(id=1)
        expected_response = None

        # When
        response = self.async_loop(pydiator.send(request))

        # Then
        assert response == expected_response
