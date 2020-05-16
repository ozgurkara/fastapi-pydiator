import asyncio
from unittest import TestCase, mock
from app.pydiator.mediatr import pydiator
from app.pydiator.mediatr_container import MediatrContainer
from app.resources.todo.handlers.delete_todo_by_id_handler import \
    DeleteTodoByIdRequest, DeleteTodoByIdResponse, DeleteTodoByIdHandler


class TestDeleteTodoByIdHandler(TestCase):

    @mock.patch("app.resources.todo.handlers.delete_todo_by_id_handler.pydiator")
    @mock.patch("app.resources.todo.handlers.delete_todo_by_id_handler.fake_todo_db")
    def test_handler_return_success(self, mock_fake_todo_db, mock_pydiator):
        # Given
        mock_fake_todo_db.__iter__.return_value = [{"id": 1, "title": "title 1"}]
        f = asyncio.Future()
        f.set_result(True)
        mock_pydiator.publish.return_value = f
        container = MediatrContainer()
        container.register_request(DeleteTodoByIdRequest(), DeleteTodoByIdHandler())
        pydiator.set_container(container)

        id = 1
        request = DeleteTodoByIdRequest(id=id)
        expected_response = DeleteTodoByIdResponse(success=True)
        loop = asyncio.new_event_loop()

        # When
        response = loop.run_until_complete(pydiator.send(request))
        loop.close()

        # Then
        assert response == expected_response
        assert mock_fake_todo_db.remove.called
        assert mock_fake_todo_db.remove.call_count == 1
        assert mock_pydiator.publish.called

    @mock.patch("app.resources.todo.handlers.delete_todo_by_id_handler.pydiator")
    @mock.patch("app.resources.todo.handlers.delete_todo_by_id_handler.fake_todo_db")
    def test_handler_return_success_false(self, mock_fake_todo_db, mock_pydiator):
        # Given
        mock_fake_todo_db.__iter__.return_value = []
        f = asyncio.Future()
        f.set_result(True)
        mock_pydiator.publish.return_value = f
        container = MediatrContainer()
        container.register_request(DeleteTodoByIdRequest(), DeleteTodoByIdHandler())
        pydiator.set_container(container)

        id = 1
        request = DeleteTodoByIdRequest(id=id)
        expected_response = DeleteTodoByIdResponse(success=False)
        loop = asyncio.new_event_loop()

        # When
        response = loop.run_until_complete(pydiator.send(request))
        loop.close()

        # Then
        assert response == expected_response
        assert mock_pydiator.publish.called is False
