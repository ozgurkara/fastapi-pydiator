import asyncio
from unittest import mock
from app.data.todo.handlers.add_todo_data_handler import AddTodoDataResponse
from app.resources.todo.handlers.add_todo_handler import \
    AddTodoRequest, AddTodoResponse, AddTodoHandler
from app.pydiator.mediatr import pydiator
from app.pydiator.mediatr_container import MediatrContainer
from tests.base_test_case import BaseTestCase


class TestAddTodoHandler(BaseTestCase):

    @mock.patch("app.resources.todo.handlers.add_todo_handler.pydiator")
    def test_handler_return_success(self, mock_pydiator):
        # Given
        container = MediatrContainer()
        container.register_request(AddTodoRequest(), AddTodoHandler())
        pydiator.set_container(container)

        mock_pydiator.send.side_effect = [self.async_return(AddTodoDataResponse(success=True))]
        mock_pydiator.publish.side_effect = [self.async_return(True)]

        title_val = "title"
        request = AddTodoRequest(title=title_val)
        expected_response = AddTodoResponse(success=True)

        # When
        response = self.async_loop(pydiator.send(request))

        # Then
        assert response == expected_response
        assert mock_pydiator.send.called
        assert mock_pydiator.publish.called

    @mock.patch("app.resources.todo.handlers.add_todo_handler.pydiator")
    def test_handler_return_fail(self, mock_pydiator):
        # Given
        container = MediatrContainer()
        container.register_request(AddTodoRequest(), AddTodoHandler())
        pydiator.set_container(container)

        mock_pydiator.send.side_effect = [self.async_return(AddTodoDataResponse(success=False))]

        title_val = "title"
        request = AddTodoRequest(title=title_val)
        expected_response = AddTodoResponse(success=False)

        # When
        response = self.async_loop(pydiator.send(request))

        # Then
        assert response == expected_response
        assert mock_pydiator.send.called
        assert mock_pydiator.publish.called is False
