from unittest import mock
from pydiator_core.mediatr import pydiator
from app.data.todo.usecases.add_todo_data import AddTodoDataResponse
from app.resources.todo.usecases.add_todo import AddTodoRequest, AddTodoResponse, AddTodoUseCase
from tests.unit.base_test_case import BaseTestCase


class TestAddTodoUseCase(BaseTestCase):

    def setUp(self):
        self.register_request(AddTodoRequest(), AddTodoUseCase())

    @mock.patch("app.resources.todo.usecases.add_todo.pydiator")
    def test_handle_return_success(self, mock_pydiator):
        # Given
        mock_pydiator.send.side_effect = [self.async_return(AddTodoDataResponse(success=True, id=1))]
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

    @mock.patch("app.resources.todo.usecases.add_todo.pydiator")
    def test_handle_return_success_false_when_data_response_is_not_successful(self, mock_pydiator):
        # Given
        mock_pydiator.send.side_effect = [self.async_return(AddTodoDataResponse(success=False, id=0))]

        title_val = "title"
        request = AddTodoRequest(title=title_val)
        expected_response = AddTodoResponse(success=False)

        # When
        response = self.async_loop(pydiator.send(request))

        # Then
        assert response == expected_response
        assert mock_pydiator.send.called
        assert mock_pydiator.publish.called is False
