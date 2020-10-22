import asyncio
from unittest import TestCase, mock
from app.data.todo.handlers.add_todo_data_handler import AddTodoDataResponse
from app.resources.todo.handlers.add_todo_handler import \
    AddTodoRequest, AddTodoResponse, AddTodoHandler
from app.pydiator.mediatr import pydiator
from app.pydiator.mediatr_container import MediatrContainer


class TestAddTodoHandler(TestCase):
    @staticmethod
    def async_return(result):
        f = asyncio.Future()
        f.set_result(result)
        return f

    @mock.patch("app.resources.todo.handlers.add_todo_handler.pydiator")
    def test_handler_return_success(self, mock_pydiator):
        # Given
        container = MediatrContainer()
        container.register_request(AddTodoRequest(), AddTodoHandler())
        pydiator.set_container(container)

        mock_pydiator.publish.side_effect = [self.async_return(True)]
        mock_pydiator.send.side_effect = [self.async_return(AddTodoDataResponse(success=True))]

        title_val = "title"
        request = AddTodoRequest(title=title_val)
        expected_response = AddTodoResponse(success=True)
        loop = asyncio.new_event_loop()

        # When
        response = loop.run_until_complete(pydiator.send(request))
        loop.close()

        # Then
        assert response == expected_response
        assert mock_pydiator.send.called
        assert mock_pydiator.publish.called

    @mock.patch("app.resources.todo.handlers.add_todo_handler.pydiator")
    def test_handler_return_fail(self, mock_pydiator):
        # Given
        mock_pydiator.send.side_effect = [self.async_return(AddTodoDataResponse(success=False))]

        container = MediatrContainer()
        container.register_request(AddTodoRequest(), AddTodoHandler())
        pydiator.set_container(container)

        title_val = "title"
        request = AddTodoRequest(title=title_val)
        expected_response = AddTodoResponse(success=False)
        loop = asyncio.new_event_loop()

        # When
        response = loop.run_until_complete(pydiator.send(request))
        loop.close()

        # Then
        assert response == expected_response
        assert mock_pydiator.send.called

#        def async_return(result):
#            f = asyncio.Future()
#            f.set_result(result)
#            return f
#
#        def async_send_side_effect(*args):
#            result = None
#            if isinstance(args[0], AddTodoDataRequest):
#                if args[0].title == "title":
#                    result = AddTodoDataResponse(success=True)
#                else:
#                    result = AddTodoDataResponse(success=False)
#            return async_return(result)
#
