from flask import Flask, jsonify, render_template, request

from db import get_db
from models import Todo
from utils import status_error, status_success
from validators import TodoValidator

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


def get_all_todos():
    with get_db() as db:
        return db.query(Todo).all()


@app.route("/api/todolist", methods=["GET"])
def api_todolist_get():
    return jsonify(
        [
            {"id": t.id, "name": t.name, "completed": t.completed}
            for t in get_all_todos()
        ]
    )


def insert_todo(name):
    with get_db() as db:
        db.add(Todo(name=name))
        db.commit()


@app.route("/api/todolist", methods=["POST"])
def api_todolist_post():
    try:
        request_dict = request.get_json()
        tv = TodoValidator(name=request_dict["name"])
        insert_todo(name=tv.name)
        return jsonify(status_success())
    except Exception as ex:
        return jsonify(status_error(ex))


def delete_todos(ids):
    with get_db() as db:
        db.query(Todo).filter(Todo.id.in_(ids)).delete()
        db.commit()


@app.route("/api/todolist", methods=["DELETE"])
def api_todolist_delete():
    try:
        request_dict = request.get_json()
        delete_todos(ids=request_dict["ids"])
        return jsonify(status_success())
    except Exception as ex:
        return jsonify(status_error(ex))


def done_todos(ids):
    with get_db() as db:
        todos = db.query(Todo).filter(Todo.id.in_(ids)).all()
        for t in todos:
            t.completed = True
        db.commit()


@app.route("/api/todolist/done", methods=["POST"])
def api_todolist_done_post():
    try:
        request_dict = request.get_json()
        done_todos(ids=request_dict["ids"])
        return jsonify(status_success())
    except Exception as ex:
        return jsonify(status_error(ex))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)
