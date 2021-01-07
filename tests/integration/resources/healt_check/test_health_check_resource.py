from starlette.status import HTTP_200_OK


class TestTodo:

    def test_get(self, test_app):
        response = test_app.get("/health-check")

        assert response.status_code == HTTP_200_OK
        assert response.content == b"OK"
