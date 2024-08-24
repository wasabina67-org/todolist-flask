from flask import Flask, jsonify, render_template, request

from db import get_db
from models import Todo
from utils import status_success, status_error
from validators import TodoValidator

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/todolist", methods=["GET"])
def api_todolist_get():
    with get_db() as db:
        todos = db.query(Todo).all()
        print(todos)

    e1 = {"id": 1, "name": "task-1", "completed": False}
    e2 = {"id": 2, "name": "task-2", "completed": True}
    e3 = {"id": 3, "name": "task-3", "completed": False}
    e4 = {"id": 4, "name": "task-4", "completed": True}
    d = [e1, e2, e3, e4]
    return jsonify(d)


@app.route("/api/todolist", methods=["POST"])
def api_todolist_post():
    try:
        request_dict = request.get_json()
        tv = TodoValidator(name=request_dict["name"])
        with get_db() as db:
            db.add(Todo(name=tv.name))
            db.commit()
        return jsonify(status_success())
    except Exception as ex:
        return jsonify(status_error(ex))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)
