import asyncio
from unittest import TestCase, mock
from app.resources.todo.handlers.update_todo_handler import \
    UpdateTodoRequest, UpdateTodoResponse, UpdateTodoHandler
from app.pydiator.mediatr import pydiator
from app.pydiator.mediatr_container import MediatrContainer


class TestAddTodoHandler(TestCase):

    @mock.patch("app.resources.todo.handlers.update_todo_handler.pydiator")
    @mock.patch("app.resources.todo.handlers.update_todo_handler.fake_todo_db")
    def test_handler_return_success(self, mock_fake_todo_db, mock_pydiator):
        # Given
        id = 1
        mock_fake_todo_db.__iter__.return_value = [{"id": id, "title": "title 1"}]
        f = asyncio.Future()
        f.set_result(True)
        mock_pydiator.publish.return_value = f
        container = MediatrContainer()
        container.register_request(UpdateTodoRequest(), UpdateTodoHandler())
        pydiator.set_container(container)

        title_val = "title 1 updated"
        request = UpdateTodoRequest(title=title_val)
        request.CustomFields.id = id
        expected_response = UpdateTodoResponse(success=True)
        loop = asyncio.new_event_loop()

        # When
        response = loop.run_until_complete(pydiator.send(request))
        loop.close()

        # Then
        assert response == expected_response
        assert mock_pydiator.publish.called

    @mock.patch("app.resources.todo.handlers.update_todo_handler.pydiator")
    @mock.patch("app.resources.todo.handlers.update_todo_handler.fake_todo_db")
    def test_handler_return_success_false(self, mock_fake_todo_db, mock_pydiator):
        # Given
        id = 1
        mock_fake_todo_db.__iter__.return_value = []
        container = MediatrContainer()
        container.register_request(UpdateTodoRequest(), UpdateTodoHandler())
        pydiator.set_container(container)

        title_val = "title 1 updated"
        request = UpdateTodoRequest(title=title_val)
        request.CustomFields.id = id
        expected_response = UpdateTodoResponse(success=False)
        loop = asyncio.new_event_loop()

        # When
        response = loop.run_until_complete(pydiator.send(request))
        loop.close()

        # Then
        assert response == expected_response
        assert mock_pydiator.publish.called is False
