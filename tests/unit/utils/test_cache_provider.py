from unittest import mock

from pytest import raises

from app.utils.cache_provider import CacheProvider
from tests.unit.base_test_case import BaseTestCase


class TestCacheProvider(BaseTestCase):
    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def test_add(self):
        # Given
        mock_client = mock.MagicMock()
        prefix = "prefix"
        provider = CacheProvider(client=mock_client, key_prefix=prefix)

        # When
        provider.add(key="key", value="val", expires=10)

        # Then
        assert mock_client.set.called
        assert mock_client.set.call_count == 1
        assert mock_client.set.call_args.args[0] == "prefix:key"
        assert mock_client.set.call_args.args[1] == "val"
        assert mock_client.set.call_args.kwargs['ex'] == 10

    def test_get(self):
        # Given
        mock_client = mock.MagicMock()
        mock_client.get.return_value = "val"
        prefix = "prefix"
        provider = CacheProvider(client=mock_client, key_prefix=prefix)

        # When
        response = provider.get(key="key")

        # Then
        assert response == "val"
        assert mock_client.get.called
        assert mock_client.get.call_count == 1
        assert mock_client.get.call_args.args[0] == "prefix:key"

    def test_exist(self):
        # Given
        mock_client = mock.MagicMock()
        mock_client.exists.return_value = True
        prefix = "prefix"
        provider = CacheProvider(client=mock_client, key_prefix=prefix)

        # When
        response = provider.exist(key="key")

        # Then
        assert response
        assert mock_client.exists.called
        assert mock_client.exists.call_count == 1
        assert mock_client.exists.call_args.args[0] == "prefix:key"

    def test_delete(self):
        # Given
        mock_client = mock.MagicMock()
        mock_client.delete.return_value = True
        prefix = "prefix"
        provider = CacheProvider(client=mock_client, key_prefix=prefix)

        # When
        provider.delete(key="key")

        # Then
        assert mock_client.delete.called
        assert mock_client.delete.call_count == 1
        assert mock_client.delete.call_args.args[0] == "prefix:key"

    def test_check_connection_is_success(self):
        # Given
        mock_client = mock.MagicMock()
        mock_client.echo.return_value = b'echo'
        prefix = "prefix"
        provider = CacheProvider(client=mock_client, key_prefix=prefix)

        # When
        response = provider.check_connection()

        # Then
        assert response
        assert mock_client.echo.called
        assert mock_client.echo.call_count == 1

    def test_check_connection_is_not_success(self):
        # Given
        mock_client = mock.MagicMock()
        mock_client.echo.return_value = b''
        prefix = "prefix"
        provider = CacheProvider(client=mock_client, key_prefix=prefix)

        # When
        response = provider.check_connection()

        # Then
        assert response is False
        assert mock_client.echo.called
        assert mock_client.echo.call_count == 1

    def test_get_client_throw_exception_when_client_is_none(self):
        # Given
        mock_client = mock.MagicMock()
        mock_client.echo.return_value = b''
        prefix = "prefix"
        provider = CacheProvider(client=None, key_prefix=prefix)

        # When
        with raises(Exception) as exc:
            provider.check_connection()

        # Then
        assert exc.value.args[0] == 'CacheProvider:client is None'
