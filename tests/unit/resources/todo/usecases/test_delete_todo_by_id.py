from unittest import mock

from app.data.todo.usecases.delete_todo_by_id_data import DeleteTodoByIdDataResponse
from pydiator_core.mediatr import pydiator
from app.resources.todo.usecases.delete_todo_by_id import \
    DeleteTodoByIdRequest, DeleteTodoByIdResponse, DeleteTodoByIdUseCase
from tests.unit.base_test_case import BaseTestCase


class TestDeleteTodoByIdUseCase(BaseTestCase):

    def setUp(self):
        self.register_request(DeleteTodoByIdRequest(), DeleteTodoByIdUseCase())

    @mock.patch("app.resources.todo.usecases.delete_todo_by_id.pydiator")
    def test_handle_return_success(self, mock_pydiator):
        # Given
        mock_pydiator.send.side_effect = [self.async_return(DeleteTodoByIdDataResponse(success=True))]
        mock_pydiator.publish.side_effect = [self.async_return(True)]

        id_val = 1
        request = DeleteTodoByIdRequest(id=id_val)
        expected_response = DeleteTodoByIdResponse(success=True)

        # When
        response = self.async_loop(pydiator.send(request))

        # Then
        assert response == expected_response
        assert mock_pydiator.send.called
        assert mock_pydiator.publish.called

    @mock.patch("app.resources.todo.usecases.delete_todo_by_id.pydiator")
    def test_handle_return_false_when_data_response_is_not_successful(self, mock_pydiator):
        # Given
        mock_pydiator.send.side_effect = [self.async_return(DeleteTodoByIdDataResponse(success=False))]
        request = DeleteTodoByIdRequest(id=1)
        expected_response = DeleteTodoByIdResponse(success=False)

        # When
        response = self.async_loop(pydiator.send(request))

        # Then
        assert response == expected_response
        assert mock_pydiator.send.called
        assert mock_pydiator.publish.called is False
