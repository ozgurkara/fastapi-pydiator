from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == "hello pydiator"


def test_get_todo_all():
    response = client.get("/v1/todo")
    items = response.json()

    assert response.status_code == 200
    assert len(items) == 2
    assert items[0]["id"] == 1
    assert items[0]["title"] == "title 1"
    assert items[1]["id"] == 2
    assert items[1]["title"] == "title 2"


def test_get_todo_by_id():
    response = client.get("/v1/todo/1")

    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert response.json()["title"] == "title 1"


def test_ad_todo():
    response = client.post("/v1/todo", json={
        "title": "title 3"
    })

    assert response.status_code == 200
    assert response.json()["success"]


def test_update_todo():
    response = client.put("/v1/todo/1", json={
        "title": "title 1 updated"
    })

    print(response)
    assert response.status_code == 200
    assert response.json()["success"]


def test_delete_todo():
    response = client.delete("/v1/todo/1")

    assert response.status_code == 200
    assert response.json()["success"]
