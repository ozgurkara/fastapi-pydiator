import asyncio
from unittest import TestCase, mock

from app.data.todo.handlers.delete_todo_by_id_data_handler import DeleteTodoByIdDataRequest, DeleteTodoByIdDataHandler, \
    DeleteTodoByIdDataResponse
from app.pydiator.mediatr import pydiator
from app.pydiator.mediatr_container import MediatrContainer
from app.resources.todo.handlers.delete_todo_by_id_handler import \
    DeleteTodoByIdRequest, DeleteTodoByIdResponse, DeleteTodoByIdHandler
from tests.BaseTestCase import BaseTestCase


class TestDeleteTodoByIdHandler(BaseTestCase):

    @mock.patch("app.data.todo.handlers.delete_todo_by_id_data_handler.fake_todo_db")
    def test_handler_return_success(self, mock_fake_todo_db):
        # Given
        container = MediatrContainer()
        container.register_request(DeleteTodoByIdDataRequest(), DeleteTodoByIdDataHandler())
        pydiator.set_container(container)

        mock_fake_todo_db.__iter__.return_value = [{"id": 1, "title": "title 1"}]

        id = 1
        request = DeleteTodoByIdDataRequest(id=id)
        expected_response = DeleteTodoByIdResponse(success=True)
        loop = asyncio.new_event_loop()

        # When
        response = loop.run_until_complete(pydiator.send(request))
        loop.close()

        # Then
        assert response == expected_response
        assert mock_fake_todo_db.remove.called
        assert mock_fake_todo_db.remove.call_count == 1

    @mock.patch("app.data.todo.handlers.delete_todo_by_id_data_handler.fake_todo_db")
    def test_handler_return_fail(self, mock_fake_todo_db):
        # Given
        container = MediatrContainer()
        container.register_request(DeleteTodoByIdDataRequest(), DeleteTodoByIdDataHandler())
        pydiator.set_container(container)

        mock_fake_todo_db.__iter__.return_value = []

        request = DeleteTodoByIdDataRequest(id=1)
        expected_response = DeleteTodoByIdDataResponse(success=False)
        loop = asyncio.new_event_loop()

        # When
        response = loop.run_until_complete(pydiator.send(request))
        loop.close()

        # Then
        assert response == expected_response
