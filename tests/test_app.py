from models import Todo  # type: ignore
from utils import status_error, status_success  # type: ignore


def test_index(client):
    rv = client.get("/")
    assert rv.status_code == 200
    assert b"<!DOCTYPE html>" in rv.data


def test_api_todolist_get(client, mocker):
    mock = mocker.patch(
        "app.get_all_todos",
        return_value=[Todo(id=1, name="task-1", completed=False)],  # noqa
    )

    rv = client.get("/api/todolist")
    assert rv.status_code == 200
    assert rv.json == [{"id": 1, "name": "task-1", "completed": False}]

    mock.assert_called()


def test_api_todolist_post(client, mocker):
    mocker.patch("app.insert_todo", return_value=None)

    rv = client.post("/api/todolist", json={"name": "a" * 80})
    assert rv.status_code == 200
    assert rv.json == status_success()


def test_api_todolist_post_error(client, mocker):
    mocker.patch("app.insert_todo", return_value=None)

    rv = client.post("/api/todolist", json={"name": ""})
    assert rv.status_code == 200
    assert rv.json == status_error("Todo must be a non-empty string.")


def test_api_todolist_post_error_2(client, mocker):
    mocker.patch("app.insert_todo", return_value=None)

    rv = client.post("/api/todolist", json={"name": "a" * 81})
    assert rv.status_code == 200
    assert rv.json == status_error(
        "Todo must not be longer than 80 characters."
    )  # noqa


def test_api_todolist_delete(client, mocker):
    mocker.patch("app.delete_todos", return_value=None)

    rv = client.delete("/api/todolist", json={"ids": [1, 2, 3]})
    assert rv.status_code == 200
    assert rv.json == status_success()


def test_api_todolist_done_post(client, mocker):
    mocker.patch("app.done_todos", return_value=None)

    rv = client.post("/api/todolist/done", json={"ids": [1, 2, 3]})
    assert rv.status_code == 200
    assert rv.json == status_success()
