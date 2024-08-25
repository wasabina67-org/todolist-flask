from models import Todo  # type: ignore
from utils import status_error, status_success  # type: ignore


def test_index(client):
    rv = client.get("/")
    assert rv.status_code == 200
    assert b"<!DOCTYPE html>" in rv.data


def test_api_todolist_get(client, mocker):
    mock_db = mocker.patch("app.get_db")

    rv = client.get("/api/todolist")
    assert rv.status_code == 200
    assert rv.json == []

    mock_db.assert_called_once()


def test_api_todolist_post(client, mocker):
    mock_db = mocker.patch("app.get_db")

    name = "a" * 80
    rv = client.post("/api/todolist", json={"name": name})
    assert rv.status_code == 200
    assert rv.json == status_success()

    mock_db.assert_called_once()
    db_instance = mock_db.return_value.__enter__.return_value
    todo_instance = db_instance.add.call_args[0][0]
    assert isinstance(todo_instance, Todo)
    assert todo_instance.name == name
    db_instance.commit.assert_called_once()


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
