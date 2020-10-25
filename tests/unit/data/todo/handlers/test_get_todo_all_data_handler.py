from unittest import mock

from app.data.todo.handlers.get_todo_all_data_handler import GetTodoAllDataRequest, GetTodoAllDataResponse, \
    GetTodoAllDataHandler
from app.pydiator.interfaces import CacheType
from app.pydiator.mediatr import pydiator
from app.resources.todo.handlers.get_todo_all_handler import GetTodoAllRequest
from tests.base_test_case import BaseTestCase


class TestGetTodoByIdHandler(BaseTestCase):
    def setUp(self):
        self.register_request(GetTodoAllDataRequest(), GetTodoAllDataHandler())

    def test_request_cache_parameter(self):
        # When
        request = GetTodoAllRequest()

        # Then
        assert request.get_cache_key() == "GetTodoAllRequest"
        assert request.get_cache_duration() == 600
        assert request.get_cache_type() == CacheType.DISTRIBUTED

    @mock.patch("app.data.todo.handlers.get_todo_all_data_handler.fake_todo_db")
    def test_handler_return_list(self, mock_fake_todo_db):
        # Give
        id_val = 1
        title_val = "title 1"
        mock_fake_todo_db.__iter__.return_value = [{"id": id_val, "title": title_val}]

        request = GetTodoAllDataRequest()
        expected_response = [GetTodoAllDataResponse(id=id_val, title=title_val)]

        # When
        response = self.async_loop(pydiator.send(request))

        # Then
        assert response == expected_response

    @mock.patch("app.data.todo.handlers.get_todo_all_data_handler.fake_todo_db")
    def test_handler_return_empty_list(self, mock_fake_todo_db):
        # Given
        mock_fake_todo_db.__iter__.return_value = []
        request = GetTodoAllDataRequest()
        expected_response = []

        # When
        response = self.async_loop(pydiator.send(request))

        # Then
        assert response == expected_response
