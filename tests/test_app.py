def test_index(client):
    rv = client.get("/")
    assert rv.status_code == 200
    assert b"<!DOCTYPE html>" in rv.data


def test_api_todolist_get(client):
    rv = client.get("/api/todolist")
    assert rv.status_code == 200
