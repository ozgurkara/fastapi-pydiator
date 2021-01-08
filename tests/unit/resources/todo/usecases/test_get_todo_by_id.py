from unittest import mock

from pytest import raises

from app.data.todo.usecases.get_todo_by_id_data import GetTodoByIdDataResponse
from pydiator_core.mediatr import pydiator
from app.resources.todo.usecases.get_todo_by_id import \
    GetTodoByIdRequest, GetTodoByIdResponse, GetTodoByIdUseCase
from app.utils.error.error_models import ErrorInfoContainer
from app.utils.exception.exception_types import ServiceException
from tests.unit.base_test_case import BaseTestCase


class TestGetTodoByIdUseCase(BaseTestCase):
    def setUp(self):
        self.register_request(GetTodoByIdRequest(), GetTodoByIdUseCase())

    @mock.patch("app.resources.todo.usecases.get_todo_by_id.pydiator")
    def test_handle_return_todo(self, mock_pydiator):
        # Given
        id_val = 1
        title_val = "title 1"
        mock_pydiator.send.side_effect = [self.async_return(GetTodoByIdDataResponse(id=id_val, title=title_val))]

        request = GetTodoByIdRequest(id=id_val)
        expected_response = GetTodoByIdResponse(id=id_val, title=title_val)

        # When
        response = self.async_loop(pydiator.send(request))

        # Then
        assert response == expected_response

    @mock.patch("app.resources.todo.usecases.get_todo_by_id.pydiator")
    def test_handle_return_none_when_data_response_is_none(self, mock_pydiator):
        # Given
        mock_pydiator.send.side_effect = [self.async_return(None)]
        request = GetTodoByIdRequest(id=1)

        # When
        with raises(ServiceException) as exc:
            self.async_loop(pydiator.send(request))

        # Then
        assert exc.value.error_info == ErrorInfoContainer.todo_not_found_error
