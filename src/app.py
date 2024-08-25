from flask import Flask, jsonify, render_template, request

from db import get_db
from models import Todo
from utils import status_error, status_success
from validators import TodoValidator

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/todolist", methods=["GET"])
def api_todolist_get():
    with get_db() as db:
        return jsonify(
            [
                {"id": t.id, "name": t.name, "completed": t.completed}
                for t in db.query(Todo).all()
            ]
        )


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


@app.route("/api/todolist", methods=["DELETE"])
def api_todolist_delete():
    return


@app.route("/api/todolist/done", methods=["POST"])
def api_todolist_done_post():
    try:
        request_dict = request.get_json()
        with get_db() as db:
            todos = db.query(Todo).filter(
                Todo.id.in_(request_dict["ids"])
            ).all()
            for t in todos:
                t.completed = True
            db.commit()
        return jsonify(status_success())
    except Exception as ex:
        return jsonify(status_error(ex))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)
