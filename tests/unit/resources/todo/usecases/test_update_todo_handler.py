from unittest import mock

from app.data.todo.usecases.update_todo_data import UpdateTodoDataResponse
from app.resources.todo.usecases.update_todo import \
    UpdateTodoRequest, UpdateTodoResponse, UpdateTodoUseCase
from pydiator_core.mediatr import pydiator
from tests.base_test_case import BaseTestCase


class TestAddTodoHandler(BaseTestCase):
    def setUp(self):
        self.register_request(UpdateTodoRequest(), UpdateTodoUseCase())

    @mock.patch("app.resources.todo.usecases.update_todo.pydiator")
    def test_handler_return_success(self, mock_pydiator):
        # Given
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

    @mock.patch("app.resources.todo.usecases.update_todo.pydiator")
    def test_handler_return_fail(self, mock_pydiator):
        # Given
        self.register_request(UpdateTodoRequest(), UpdateTodoUseCase())
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
