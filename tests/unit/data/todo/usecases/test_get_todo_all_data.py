from unittest import mock

from app.data.todo.usecases.get_todo_all_data import GetTodoAllDataRequest, GetTodoAllDataResponse, \
    GetTodoAllDataUseCase
from pydiator_core.interfaces import CacheType
from pydiator_core.mediatr import pydiator
from app.resources.todo.usecases.get_todo_all import GetTodoAllRequest
from tests.unit.base_test_case import BaseTestCase


class TestGetTodoAllDataUseCase(BaseTestCase):
    def setUp(self):
        self.register_request(GetTodoAllDataRequest(), GetTodoAllDataUseCase())

    def test_request_cache_parameter(self):
        # When
        request = GetTodoAllRequest()

        # Then
        assert request.get_cache_key() == "GetTodoAllRequest"
        assert request.get_cache_duration() == 600
        assert request.get_cache_type() == CacheType.DISTRIBUTED

    @mock.patch("app.data.todo.usecases.get_todo_all_data.fake_todo_db")
    def test_handle_return_list(self, mock_fake_todo_db):
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

    @mock.patch("app.data.todo.usecases.get_todo_all_data.fake_todo_db")
    def test_handle_return_empty_list(self, mock_fake_todo_db):
        # Given
        mock_fake_todo_db.__iter__.return_value = []
        request = GetTodoAllDataRequest()
        expected_response = []

        # When
        response = self.async_loop(pydiator.send(request))

        # Then
        assert response == expected_response
