import asyncio
from unittest import TestCase, mock

from app.data.todo.handlers.add_todo_data_handler import AddTodoDataHandler, AddTodoDataRequest, AddTodoDataResponse
from app.pydiator.mediatr import pydiator
from app.pydiator.mediatr_container import MediatrContainer


class TestAddTodoDataHandler(TestCase):
    @staticmethod
    def async_return(result):
        f = asyncio.Future()
        f.set_result(result)
        return f

    @mock.patch("app.data.todo.handlers.add_todo_data_handler.fake_todo_db")
    def test_handler_return_success(self, mock_fake_todo_db):
        # Given
        container = MediatrContainer()
        container.register_request(AddTodoDataRequest(), AddTodoDataHandler())
        pydiator.set_container(container)

        mock_fake_todo_db.__iter__.return_value = []

        title_val = "title"
        request = AddTodoDataRequest(title=title_val)
        expected_response = AddTodoDataResponse(success=True)
        loop = asyncio.new_event_loop()

        # When
        response = loop.run_until_complete(pydiator.send(request))
        loop.close()

        # Then
        assert response == expected_response
        assert mock_fake_todo_db.append.call_count == 1
        assert mock_fake_todo_db.append.called
