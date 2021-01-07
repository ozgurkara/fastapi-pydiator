from starlette.status import HTTP_200_OK

from tests.integration.integration_test_helper import  client


class TestTodo:

    def test_get(self):
        response = client.get("/health-check")

        assert response.status_code == HTTP_200_OK
        assert response.content == b"OK"
