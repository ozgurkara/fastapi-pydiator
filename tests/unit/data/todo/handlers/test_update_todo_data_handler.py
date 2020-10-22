import asyncio
from unittest import mock

from app.data.todo.handlers.update_todo_data_handler import UpdateTodoDataHandler, UpdateTodoDataRequest, \
    UpdateTodoDataResponse
from app.pydiator.mediatr import pydiator
from app.pydiator.mediatr_container import MediatrContainer
from tests.base_test_case import BaseTestCase


class TestAddTodoHandler(BaseTestCase):

    @mock.patch("app.data.todo.handlers.update_todo_data_handler.fake_todo_db")
    def test_handler_return_success(self, mock_fake_todo_db):
        # Given
        container = MediatrContainer()
        container.register_request(UpdateTodoDataRequest(), UpdateTodoDataHandler())
        pydiator.set_container(container)

        id_val = 1
        mock_fake_todo_db.__iter__.return_value = [{"id": id_val, "title": "title 1"}]

        title_val = "title 1 updated"
        request = UpdateTodoDataRequest(title=title_val)
        request.id = id_val
        expected_response = UpdateTodoDataResponse(success=True)
        loop = asyncio.new_event_loop()

        # When
        response = loop.run_until_complete(pydiator.send(request))
        loop.close()

        # Then
        assert response == expected_response

    @mock.patch("app.data.todo.handlers.update_todo_data_handler.fake_todo_db")
    def test_handler_return_fail(self, mock_fake_todo_db):
        # Given

        container = MediatrContainer()
        container.register_request(UpdateTodoDataRequest(), UpdateTodoDataHandler())
        pydiator.set_container(container)

        mock_fake_todo_db.__iter__.return_value = []
        title_val = "title 1 updated"
        request = UpdateTodoDataRequest(title=title_val)
        request.id = id
        expected_response = UpdateTodoDataResponse(success=False)
        loop = asyncio.new_event_loop()

        # When
        response = loop.run_until_complete(pydiator.send(request))
        loop.close()

        # Then
        assert response == expected_response
