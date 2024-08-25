from models import Todo  # type: ignore


def test_index(client):
    rv = client.get("/")
    assert rv.status_code == 200
    assert b"<!DOCTYPE html>" in rv.data


def test_api_todolist_get(client, mocker):
    mocker.patch(
        "app.get_all_todos",
        return_value=[Todo(id=1, name="task-1", completed=False)],  # noqa
    )

    rv = client.get("/api/todolist")
    assert rv.status_code == 200
    assert rv.json == [{"id": 1, "name": "task-1", "completed": False}]
