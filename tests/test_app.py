from models import Todo  # type: ignore
from utils import status_error, status_success  # type: ignore


def test_index(client):
    rv = client.get("/")
    assert rv.status_code == 200
    assert b"<!DOCTYPE html>" in rv.data


def test_api_todolist_get_empty(client, mocker):
    mock_db = mocker.patch("app.get_db")

    rv = client.get("/api/todolist")
    assert rv.status_code == 200
    assert rv.json == []

    mock_db.assert_called_once()


def test_api_todolist_get_has_rec(client, mocker):
    mock = mocker.patch(
        "app.get_all_todos",
        return_value=[
            Todo(id=1, name="task-1", completed=False),
            Todo(id=2, name="task-2", completed=True),
            Todo(id=3, name="task-3", completed=True),
            Todo(id=4, name="task-4", completed=False),
            Todo(id=5, name="task-5", completed=True),
        ],
    )

    rv = client.get("/api/todolist")
    assert rv.status_code == 200
    assert rv.json == [
        {"id": 1, "name": "task-1", "completed": False},
        {"id": 2, "name": "task-2", "completed": True},
        {"id": 3, "name": "task-3", "completed": True},
        {"id": 4, "name": "task-4", "completed": False},
        {"id": 5, "name": "task-5", "completed": True},
    ]

    mock.assert_called_once()


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


def test_api_todolist_post_error_empty(client, mocker):
    mock = mocker.patch("app.insert_todo", return_value=None)

    rv = client.post("/api/todolist", json={"name": ""})
    assert rv.status_code == 200
    assert rv.json == status_error("Todo must be a non-empty string.")

    mock.assert_not_called()


def test_api_todolist_post_error_too_long(client, mocker):
    mock = mocker.patch("app.insert_todo", return_value=None)

    rv = client.post("/api/todolist", json={"name": "a" * 81})
    assert rv.status_code == 200
    assert rv.json == status_error(
        "Todo must not be longer than 80 characters."
    )  # noqa

    mock.assert_not_called()


def test_api_todolist_delete_commit_once(client, mocker):
    mock_db = mocker.patch("app.get_db")

    ids = [1, 2, 3]
    rv = client.delete("/api/todolist", json={"ids": ids})
    assert rv.status_code == 200
    assert rv.json == status_success()

    mock_db.assert_called_once()
    db_instance = mock_db.return_value.__enter__.return_value
    db_instance.commit.assert_called_once()


def test_api_todolist_delete_check_args(client, mocker):
    mock = mocker.patch("app.delete_todos", return_value=None)

    ids = [4, 5, 6]
    rv = client.delete("/api/todolist", json={"ids": ids})
    assert rv.status_code == 200
    assert rv.json == status_success()

    mock.assert_called_once_with(ids=ids)


def test_api_todolist_delete_db_error(client, mocker):
    mock = mocker.patch("app.delete_todos")
    mock.side_effect = Exception("Database error")

    ids = [7, 8, 9]
    rv = client.delete("/api/todolist", json={"ids": ids})
    assert rv.status_code == 200
    assert rv.json == status_error("Database error")

    mock.assert_called_once_with(ids=ids)


def test_api_todolist_done_post_commit_once(client, mocker):
    mock_db = mocker.patch("app.get_db")

    ids = [1, 2, 3]
    rv = client.post("/api/todolist/done", json={"ids": ids})
    assert rv.status_code == 200
    assert rv.json == status_success()

    mock_db.assert_called_once()
    db_instance = mock_db.return_value.__enter__.return_value
    db_instance.commit.assert_called_once()


def test_api_todolist_done_post_check_args(client, mocker):
    mock = mocker.patch("app.done_todos", return_value=None)

    ids = [4, 5, 6]
    rv = client.post("/api/todolist/done", json={"ids": ids})
    assert rv.status_code == 200
    assert rv.json == status_success()

    mock.assert_called_once_with(ids=ids)
