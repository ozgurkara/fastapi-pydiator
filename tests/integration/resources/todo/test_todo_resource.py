from fastapi.testclient import TestClient
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY, HTTP_200_OK

from main import app


class TestTodo:
    client = TestClient(app=app)

    def test_get_todo_all(self):
        response = self.client.get("/v1/todos")
        items = response.json()

        assert response.status_code == HTTP_200_OK
        assert len(items) == 2
        assert items[0]["id"] == 1
        assert items[0]["title"] == "title 1"
        assert items[1]["id"] == 2
        assert items[1]["title"] == "title 2"

    def test_get_todo_by_id(self):
        response = self.client.get("/v1/todos/1")

        assert response.status_code == HTTP_200_OK
        assert response.json()["id"] == 1
        assert response.json()["title"] == "title 1"

    def test_add_todo(self):
        response = self.client.post("/v1/todos", json={
            "title": "title 3"
        })

        assert response.status_code == HTTP_200_OK
        assert response.json()["success"]

    def test_add_todo_should_return_unprocessable_when_invalid_entity(self):
        response = self.client.post("/v1/todos", json=None)

        assert response.status_code == HTTP_422_UNPROCESSABLE_ENTITY

    def test_update_todo(self):
        response = self.client.put("/v1/todos/1", json={
            "title": "title 1 updated"
        })

        assert response.status_code == HTTP_200_OK
        assert response.json()["success"]

    def test_update_todo_should_return_unprocessable_when_invalid_entity(self):
        response = self.client.put("/v1/todos/1", json={

        })

        assert response.status_code == HTTP_422_UNPROCESSABLE_ENTITY

    def test_delete_todo(self):
        response = self.client.delete("/v1/todos/1")

        assert response.status_code == HTTP_200_OK
        assert response.json()["success"]
