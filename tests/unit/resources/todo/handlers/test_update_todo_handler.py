from unittest import mock

from app.data.todo.handlers.update_todo_data_handler import UpdateTodoDataResponse
from app.resources.todo.handlers.update_todo_handler import \
    UpdateTodoRequest, UpdateTodoResponse, UpdateTodoHandler
from app.pydiator.mediatr import pydiator
from app.pydiator.mediatr_container import MediatrContainer
from tests.base_test_case import BaseTestCase


class TestAddTodoHandler(BaseTestCase):
    @mock.patch("app.resources.todo.handlers.update_todo_handler.pydiator")
    def test_handler_return_success(self, mock_pydiator):
        # Given
        container = MediatrContainer()
        container.register_request(UpdateTodoRequest(), UpdateTodoHandler())
        pydiator.set_container(container)

        mock_pydiator.send.side_effect = [self.async_return(UpdateTodoDataResponse(success=True))]
        mock_pydiator.publish.side_effect = [self.async_return(True)]

        id_val = 1
        title_val = "title 1 updated"
        request = UpdateTodoRequest(title=title_val)
        request.CustomFields.id = id_val
        expected_response = UpdateTodoResponse(success=True)

        # When
        response = self.async_loop(pydiator.send(request))

        # Then
        assert response == expected_response
        assert mock_pydiator.send.called
        assert mock_pydiator.publish.called

    @mock.patch("app.resources.todo.handlers.update_todo_handler.pydiator")
    def test_handler_return_fail(self, mock_pydiator):
        # Given
        container = MediatrContainer()
        container.register_request(UpdateTodoRequest(), UpdateTodoHandler())
        pydiator.set_container(container)

        mock_pydiator.send.side_effect = [self.async_return(UpdateTodoDataResponse(success=False))]

        id_val = 1
        title_val = "title 1 updated"
        request = UpdateTodoRequest(title=title_val)
        request.CustomFields.id = id_val
        expected_response = UpdateTodoResponse(success=False)

        # When
        response = self.async_loop(pydiator.send(request))

        # Then
        assert response == expected_response
        assert mock_pydiator.send.called
        assert mock_pydiator.publish.called is False
