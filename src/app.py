from flask import Flask, jsonify, render_template

from db import get_db
from models import Todo

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/todolist", methods=["GET"])
def api_todolist_get():
    with get_db() as db:
        todos = db.query(Todo).all()
        print(todos)

    d = []
    return jsonify(d)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)
