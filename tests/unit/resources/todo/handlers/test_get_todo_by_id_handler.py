import asyncio
from unittest import TestCase, mock
from app.pydiator.mediatr import pydiator
from app.pydiator.mediatr_container import MediatrContainer
from app.resources.todo.handlers.get_todo_by_id_handler import \
    GetTodoByIdRequest, GetTodoByIdResponse, GetTodoByIdHandler


class TestGetTodoByIdHandler(TestCase):

    @mock.patch("app.resources.todo.handlers.get_todo_by_id_handler.fake_todo_db")
    def test_handler_return_todo(self, mock_fake_todo_db):
        # Given
        mock_fake_todo_db.__iter__.return_value = [{"id": 1, "title": "title 1"}]
        container = MediatrContainer()
        container.register_request(GetTodoByIdRequest(), GetTodoByIdHandler())
        pydiator.set_container(container)

        id = 1
        request = GetTodoByIdRequest(id=id)
        expected_response = GetTodoByIdResponse(id=id, title="title 1")
        loop = asyncio.new_event_loop()

        # When
        response = loop.run_until_complete(pydiator.send(request))
        loop.close()

        # Then
        assert response == expected_response

    @mock.patch("app.resources.todo.handlers.get_todo_by_id_handler.fake_todo_db")
    def test_handler_return_none(self, mock_fake_todo_db):
        # Given
        mock_fake_todo_db.__iter__.return_value = []
        container = MediatrContainer()
        container.register_request(GetTodoByIdRequest(), GetTodoByIdHandler())
        pydiator.set_container(container)
        request = GetTodoByIdRequest(id=1)
        expected_response = None
        loop = asyncio.new_event_loop()

        # When
        response = loop.run_until_complete(pydiator.send(request))
        loop.close()

        # Then
        assert response == expected_response
