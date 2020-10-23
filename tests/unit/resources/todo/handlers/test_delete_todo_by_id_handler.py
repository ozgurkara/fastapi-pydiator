import asyncio
from unittest import mock

from app.data.todo.handlers.delete_todo_by_id_data_handler import DeleteTodoByIdDataResponse
from app.pydiator.mediatr import pydiator
from app.pydiator.mediatr_container import MediatrContainer
from app.resources.todo.handlers.delete_todo_by_id_handler import \
    DeleteTodoByIdRequest, DeleteTodoByIdResponse, DeleteTodoByIdHandler
from tests.base_test_case import BaseTestCase


class TestDeleteTodoByIdHandler(BaseTestCase):

    @mock.patch("app.resources.todo.handlers.delete_todo_by_id_handler.pydiator")
    def test_handler_return_success(self, mock_pydiator):
        # Given
        container = MediatrContainer()
        container.register_request(DeleteTodoByIdRequest(), DeleteTodoByIdHandler())
        pydiator.set_container(container)

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

    @mock.patch("app.resources.todo.handlers.delete_todo_by_id_handler.pydiator")
    def test_handler_return_fail(self, mock_pydiator):
        # Given
        container = MediatrContainer()
        container.register_request(DeleteTodoByIdRequest(), DeleteTodoByIdHandler())
        pydiator.set_container(container)
        mock_pydiator.send.side_effect = [self.async_return(DeleteTodoByIdDataResponse(success=False))]
        request = DeleteTodoByIdRequest(id=1)
        expected_response = DeleteTodoByIdResponse(success=False)

        # When
        response = self.async_loop(pydiator.send(request))

        # Then
        assert response == expected_response
        assert mock_pydiator.send.called
        assert mock_pydiator.publish.called is False
