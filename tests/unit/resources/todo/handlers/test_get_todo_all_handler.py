import asyncio
from unittest import TestCase, mock

from app.data.todo.handlers.get_todo_all_data_handler import GetTodoAllDataResponse
from app.data.todo.handlers.get_todo_by_id_data_handler import GetTodoByIdDataResponse
from app.pydiator.mediatr import pydiator
from app.pydiator.mediatr_container import MediatrContainer
from app.resources.todo.handlers.get_todo_all_handler import GetTodoAllRequest, GetTodoAllHandler, GetTodoAllResponse
from app.resources.todo.handlers.get_todo_by_id_handler import \
    GetTodoByIdRequest, GetTodoByIdResponse, GetTodoByIdHandler


class TestGetTodoByIdHandler(TestCase):
    @staticmethod
    def async_return(result):
        f = asyncio.Future()
        f.set_result(result)
        return f

    @mock.patch("app.resources.todo.handlers.get_todo_all_handler.pydiator")
    def test_handler_return_list(self, mock_pydiator):
        # Given
        container = MediatrContainer()
        container.register_request(GetTodoAllRequest(), GetTodoAllHandler())
        pydiator.set_container(container)

        id_val = 1
        title_val = "title 1"
        mock_pydiator.send.side_effect = [self.async_return([GetTodoAllDataResponse(id=id_val, title=title_val)])]

        request = GetTodoAllRequest(id=id_val)
        expected_response = [GetTodoAllResponse(id=id_val, title=title_val)]
        loop = asyncio.new_event_loop()

        # When
        response = loop.run_until_complete(pydiator.send(request))
        loop.close()

        # Then
        assert response == expected_response

    @mock.patch("app.resources.todo.handlers.get_todo_all_handler.pydiator")
    def test_handler_return_empty_list(self, mock_pydiator):
        # Given
        container = MediatrContainer()
        container.register_request(GetTodoAllRequest(), GetTodoAllHandler())
        pydiator.set_container(container)

        mock_pydiator.send.side_effect = [self.async_return([])]

        request = GetTodoAllRequest(id=1)
        expected_response = []
        loop = asyncio.new_event_loop()

        # When
        response = loop.run_until_complete(pydiator.send(request))
        loop.close()

        # Then
        assert response == expected_response
