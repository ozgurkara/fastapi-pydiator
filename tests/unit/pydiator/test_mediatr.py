from unittest import mock

from app.pydiator.interfaces import BaseNotification
from app.pydiator.mediatr import Mediatr
from tests.base_test_case import BaseTestCase, TestRequest, TestResponse, FakeMediatrContainer, TestNotification


class TestMediatrContainer(BaseTestCase):

    def setUp(self):
        pass

    def test_read_default_values_when_create_instance(self):
        # Given

        # When
        mediatr = Mediatr()

        # Then
        assert mediatr.mediatr_container is None
        assert mediatr.is_ready is False

    def test_ready_when_is_ready(self):
        # Given
        mediatr = Mediatr()
        mediatr.is_ready = True

        # When
        mediatr.ready({})

        # Then
        assert mediatr.mediatr_container is None

    def test_ready_when_is_not_ready(self):
        # Given
        mediatr_container = FakeMediatrContainer()
        mediatr = Mediatr()

        # When
        mediatr.ready(mediatr_container)

        # Then
        assert mediatr.mediatr_container is mediatr_container
        assert mediatr.is_ready
        assert len(mediatr_container.get_pipelines()) == 1

    def test_send_raise_exception_when_container_is_none(self):
        # Given
        mediatr = Mediatr()

        # When
        with self.assertRaises(Exception) as context:
            self.async_loop(mediatr.send(TestRequest()))

        # Then
        assert 'mediatr_container_is_none' == context.exception.args[0]

    def test_send_raise_exception_when_container_pipelines_is_empty(self):
        # Given
        mediatr = Mediatr()
        mediatr.mediatr_container = FakeMediatrContainer()

        # When
        with self.assertRaises(Exception) as context:
            self.async_loop(mediatr.send(TestRequest()))

        # Then
        assert 'mediatr_container_has_not_contain_any_pipeline' == context.exception.args[0]

    @mock.patch("app.pydiator.mediatr.DefaultPipeline")
    def test_send_return_default_pipeline_result_when_container_pipelines_is_empty(self, mock_default_pipeline):
        # Given
        next_response = TestResponse(success=True)

        async def next_handle(req):
            return next_response

        mock_default_pipeline.return_value.handle = next_handle
        mediatr_container = FakeMediatrContainer()
        mediatr = Mediatr()
        mediatr.ready(mediatr_container)

        # When
        response = self.async_loop(mediatr.send(TestRequest()))

        # Then
        assert response is next_response
        assert response.success

    def test_publish_when_handlers_is_empty(self):
        # Given
        mediatr_container = FakeMediatrContainer()
        mediatr = Mediatr()
        mediatr_container.register_notification(TestNotification(), [])
        mediatr.ready(mediatr_container)

        # When
        with self.assertRaises(Exception) as context:
            self.async_loop(mediatr.publish(BaseNotification()))

        # Then
        assert 'mediatr_container_has_not_contain_any_notification_handler_for:BaseNotification' == \
               context.exception.args[0]

    def test_publish_when_handlers_exist(self):
        # Given
        async def next_handle(notification):
            pass

        mock_notification_handler = mock.MagicMock()
        mock_notification_handler.handle.side_effect = next_handle

        mediatr_container = FakeMediatrContainer()
        mediatr_container.register_notification(TestNotification(), [mock_notification_handler])

        mediatr = Mediatr()
        mediatr.ready(mediatr_container)

        # When
        self.async_loop(mediatr.publish(TestNotification()))

        # Then
        assert mock_notification_handler.handle.called
        assert mock_notification_handler.handle.call_count == 1

    def test_publish_when_handle_has_exception(self):
        # Given
        async def next_handle(notification):
            raise Exception("")

        mock_notification_handler = mock.MagicMock()
        mock_notification_handler.handle.side_effect = next_handle

        mediatr_container = FakeMediatrContainer()
        mediatr_container.register_notification(TestNotification(), [mock_notification_handler])

        mediatr = Mediatr()
        mediatr.ready(mediatr_container)

        # When
        self.async_loop(mediatr.publish(notification=TestNotification()))

        # Then
        assert mock_notification_handler.handle.called
        assert mock_notification_handler.handle.call_count == 1

    def test_publish_when_handle_has_exception_and_throw_exception(self):
        # Given
        async def next_handle(notification):
            raise Exception("test_exception")

        mock_notification_handler = mock.MagicMock()
        mock_notification_handler.handle.side_effect = next_handle

        mediatr_container = FakeMediatrContainer()
        mediatr_container.register_notification(TestNotification(), [mock_notification_handler])

        mediatr = Mediatr()
        mediatr.ready(mediatr_container)

        # When
        with self.assertRaises(Exception) as context:
            self.async_loop(mediatr.publish(notification=TestNotification(), throw_exception=True))

        # Then
        assert mock_notification_handler.handle.called
        assert mock_notification_handler.handle.call_count == 1
        assert 'test_exception' == context.exception.args[0]
