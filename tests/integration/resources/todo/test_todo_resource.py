from fastapi.testclient import TestClient
from app.main import app
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY, HTTP_200_OK

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == HTTP_200_OK
    assert response.json() == "hello pydiator"


def test_get_todo_all():
    response = client.get("/v1/todo")
    items = response.json()

    assert response.status_code == HTTP_200_OK
    assert len(items) == 2
    assert items[0]["id"] == 1
    assert items[0]["title"] == "title 1"
    assert items[1]["id"] == 2
    assert items[1]["title"] == "title 2"


def test_get_todo_by_id():
    response = client.get("/v1/todo/1")

    assert response.status_code == HTTP_200_OK
    assert response.json()["id"] == 1
    assert response.json()["title"] == "title 1"


def test_ad_todo():
    response = client.post("/v1/todo", json={
        "title": "title 3"
    })

    assert response.status_code == HTTP_200_OK
    assert response.json()["success"]


def test_ad_todo_bad_request_when_invalid_entity():
    response = client.post("/v1/todo", json={

    })

    assert response.status_code == HTTP_422_UNPROCESSABLE_ENTITY


def test_update_todo():
    response = client.put("/v1/todo/1", json={
        "title": "title 1 updated"
    })

    print(response)
    assert response.status_code == HTTP_200_OK
    assert response.json()["success"]


def test_update_todo_bad_request_when_invalid_entity():
    response = client.put("/v1/todo/1", json={

    })

    assert response.status_code == HTTP_422_UNPROCESSABLE_ENTITY


def test_delete_todo():
    response = client.delete("/v1/todo/1")

    assert response.status_code == HTTP_200_OK
    assert response.json()["success"]
