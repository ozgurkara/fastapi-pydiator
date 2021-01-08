from unittest import mock

from app.data.todo.usecases.delete_todo_by_id_data import DeleteTodoByIdDataRequest, DeleteTodoByIdDataUseCase, \
    DeleteTodoByIdDataResponse
from pydiator_core.mediatr import pydiator
from app.resources.todo.usecases.delete_todo_by_id import DeleteTodoByIdResponse
from tests.unit.base_test_case import BaseTestCase


class TestDeleteTodoByIdDataUseCase(BaseTestCase):
    def setUp(self):
        self.register_request(DeleteTodoByIdDataRequest(), DeleteTodoByIdDataUseCase())

    @mock.patch("app.data.todo.usecases.delete_todo_by_id_data.fake_todo_db")
    def test_handle_return_success(self, mock_fake_todo_db):
        # Given
        id_val = 1
        mock_fake_todo_db.__iter__.return_value = [{"id": id_val, "title": "title 1"}]
        request = DeleteTodoByIdDataRequest(id=id_val)
        expected_response = DeleteTodoByIdResponse(success=True)

        # When
        response = self.async_loop(pydiator.send(request))

        # Then
        assert response == expected_response
        assert mock_fake_todo_db.remove.called
        assert mock_fake_todo_db.remove.call_count == 1

    @mock.patch("app.data.todo.usecases.delete_todo_by_id_data.fake_todo_db")
    def test_handle_return_success_false_when_todo_is_not_exist(self, mock_fake_todo_db):
        # Given
        mock_fake_todo_db.__iter__.return_value = []
        request = DeleteTodoByIdDataRequest(id=1)
        expected_response = DeleteTodoByIdDataResponse(success=False)

        # When
        response = self.async_loop(pydiator.send(request))

        # Then
        assert response == expected_response
