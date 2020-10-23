from unittest import mock

from app.data.todo.handlers.get_todo_by_id_data_handler import GetTodoByIdDataHandler, GetTodoByIdDataRequest, \
    GetTodoByIdDataResponse
from app.pydiator.mediatr import pydiator
from app.pydiator.mediatr_container import MediatrContainer
from tests.base_test_case import BaseTestCase


class TestGetTodoByIdHandler(BaseTestCase):

    @mock.patch("app.data.todo.handlers.get_todo_by_id_data_handler.fake_todo_db")
    def test_handler_return_todo(self, mock_fake_todo_db):
        # Given
        container = MediatrContainer()
        container.register_request(GetTodoByIdDataRequest(), GetTodoByIdDataHandler())
        pydiator.set_container(container)

        id_val = 1
        title_val = "title 1"
        mock_fake_todo_db.__iter__.return_value = [{"id": id_val, "title": title_val}]

        request = GetTodoByIdDataRequest(id=id_val)
        expected_response = GetTodoByIdDataResponse(id=id_val, title=title_val)

        # When
        response = self.async_loop(pydiator.send(request))

        # Then
        assert response == expected_response

    @mock.patch("app.data.todo.handlers.get_todo_by_id_data_handler.fake_todo_db")
    def test_handler_return_none(self, mock_fake_todo_db):
        # Given
        container = MediatrContainer()
        container.register_request(GetTodoByIdDataRequest(), GetTodoByIdDataHandler())
        pydiator.set_container(container)

        mock_fake_todo_db.__iter__.return_value = []
        request = GetTodoByIdDataRequest(id=1)
        expected_response = None

        # When
        response = self.async_loop(pydiator.send(request))

        # Then
        assert response == expected_response
