import asyncio
from unittest import mock

from app.data.todo.handlers.get_todo_by_id_data_handler import GetTodoByIdDataResponse
from app.pydiator.mediatr import pydiator
from app.pydiator.mediatr_container import MediatrContainer
from app.resources.todo.handlers.get_todo_by_id_handler import \
    GetTodoByIdRequest, GetTodoByIdResponse, GetTodoByIdHandler
from tests.BaseTestCase import BaseTestCase


class TestGetTodoByIdHandler(BaseTestCase):

    @mock.patch("app.resources.todo.handlers.get_todo_by_id_handler.pydiator")
    def test_handler_return_todo(self, mock_pydiator):
        # Given
        container = MediatrContainer()
        container.register_request(GetTodoByIdRequest(), GetTodoByIdHandler())
        pydiator.set_container(container)

        id_val = 1
        title_val = "title 1"
        mock_pydiator.send.side_effect = [self.async_return(GetTodoByIdDataResponse(id=id_val, title=title_val))]

        request = GetTodoByIdRequest(id=id_val)
        expected_response = GetTodoByIdResponse(id=id_val, title=title_val)
        loop = asyncio.new_event_loop()

        # When
        response = loop.run_until_complete(pydiator.send(request))
        loop.close()

        # Then
        assert response == expected_response

    @mock.patch("app.resources.todo.handlers.get_todo_by_id_handler.pydiator")
    def test_handler_return_none(self, mock_pydiator):
        # Given
        container = MediatrContainer()
        container.register_request(GetTodoByIdRequest(), GetTodoByIdHandler())
        pydiator.set_container(container)

        mock_pydiator.send.side_effect = [self.async_return(None)]

        request = GetTodoByIdRequest(id=1)
        expected_response = None
        loop = asyncio.new_event_loop()

        # When
        response = loop.run_until_complete(pydiator.send(request))
        loop.close()

        # Then
        assert response == expected_response
