from unittest import mock

from pytest import raises

from app.data.todo.usecases.update_todo_data import UpdateTodoDataUseCase, UpdateTodoDataRequest, \
    UpdateTodoDataResponse
from pydiator_core.mediatr import pydiator

from app.utils.error.error_models import ErrorInfoContainer
from app.utils.exception.exception_types import DataException
from tests.unit.base_test_case import BaseTestCase


class TestUpdateTodoDataUseCase(BaseTestCase):
    def setUp(self):
        self.register_request(UpdateTodoDataRequest(), UpdateTodoDataUseCase())

    @mock.patch("app.data.todo.usecases.update_todo_data.fake_todo_db")
    def test_handle_return_success(self, mock_fake_todo_db):
        # Given
        id_val = 1
        mock_fake_todo_db.__iter__.return_value = [{"id": id_val, "title": "title 1"}]
        title_val = "title 1 updated"
        request = UpdateTodoDataRequest(title=title_val)
        request.id = id_val
        expected_response = UpdateTodoDataResponse(success=True)

        # When
        response = self.async_loop(pydiator.send(request))

        # Then
        assert response == expected_response

    @mock.patch("app.data.todo.usecases.update_todo_data.fake_todo_db")
    def test_handle_return_exception_when_todo_not_found(self, mock_fake_todo_db):
        # Given
        mock_fake_todo_db.__iter__.return_value = []
        title_val = "title 1 updated"
        request = UpdateTodoDataRequest(title=title_val)

        # When
        with raises(DataException) as exc:
            self.async_loop(pydiator.send(request))

        # Then
        assert exc.value.error_info == ErrorInfoContainer.todo_not_found_error
