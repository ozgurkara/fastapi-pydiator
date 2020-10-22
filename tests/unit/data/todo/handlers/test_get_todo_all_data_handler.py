import asyncio
from unittest import mock

from app.data.todo.handlers.get_todo_all_data_handler import GetTodoAllDataRequest, GetTodoAllDataResponse, \
    GetTodoAllDataHandler
from app.pydiator.interfaces import CacheType
from app.pydiator.mediatr import pydiator
from app.pydiator.mediatr_container import MediatrContainer
from app.resources.todo.handlers.get_todo_all_handler import GetTodoAllRequest
from tests.BaseTestCase import BaseTestCase


class TestGetTodoByIdHandler(BaseTestCase):

    def test_request_cache_parameter(self):
        # When
        request = GetTodoAllRequest()

        # Then
        assert request.get_cache_key() == "GetTodoAllRequest"
        assert request.get_cache_duration() == 600
        assert request.get_cache_type() == CacheType.DISTRIBUTED

    @mock.patch("app.data.todo.handlers.get_todo_all_data_handler.fake_todo_db")
    def test_handler_return_list(self, mock_fake_todo_db):
        # Given
        container = MediatrContainer()
        container.register_request(GetTodoAllDataRequest(), GetTodoAllDataHandler())
        pydiator.set_container(container)

        id_val = 1
        title_val = "title 1"
        mock_fake_todo_db.__iter__.return_value = [{"id": id_val, "title": title_val}]

        request = GetTodoAllDataRequest()
        expected_response = [GetTodoAllDataResponse(id=id_val, title=title_val)]
        loop = asyncio.new_event_loop()

        # When
        response = loop.run_until_complete(pydiator.send(request))
        loop.close()

        # Then
        assert response == expected_response

    @mock.patch("app.data.todo.handlers.get_todo_all_data_handler.fake_todo_db")
    def test_handler_return_empty_list(self, mock_fake_todo_db):
        # Given
        container = MediatrContainer()
        container.register_request(GetTodoAllDataRequest(), GetTodoAllDataHandler())
        pydiator.set_container(container)

        mock_fake_todo_db.__iter__.return_value = []
        request = GetTodoAllDataRequest()
        expected_response = []
        loop = asyncio.new_event_loop()

        # When
        response = loop.run_until_complete(pydiator.send(request))
        loop.close()

        # Then
        assert response == expected_response
