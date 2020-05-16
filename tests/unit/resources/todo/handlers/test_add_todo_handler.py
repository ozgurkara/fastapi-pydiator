import asyncio
from unittest import TestCase, mock
from app.resources.todo.handlers.add_todo_handler import \
    AddTodoRequest, AddTodoResponse, AddTodoHandler
from app.pydiator.mediatr import pydiator
from app.pydiator.mediatr_container import MediatrContainer


class TestAddTodoHandler(TestCase):

    @mock.patch("app.resources.todo.handlers.add_todo_handler.pydiator")
    @mock.patch("app.resources.todo.handlers.add_todo_handler.fake_todo_db")
    def test_handler_return_success(self, mock_fake_todo_db, mock_pydiator):
        # Given
        mock_fake_todo_db.__iter__.return_value = []
        f = asyncio.Future()
        f.set_result(True)
        mock_pydiator.publish.return_value = f
        container = MediatrContainer()
        container.register_request(AddTodoRequest(), AddTodoHandler())
        pydiator.set_container(container)

        title_val = "title"
        request = AddTodoRequest(title=title_val)
        expected_response = AddTodoResponse(success=True)
        loop = asyncio.new_event_loop()

        # When
        response = loop.run_until_complete(pydiator.send(request))
        loop.close()

        # Then
        assert response == expected_response
        assert mock_fake_todo_db.append.call_count == 1
        assert mock_fake_todo_db.append.called
        assert mock_pydiator.publish.called
