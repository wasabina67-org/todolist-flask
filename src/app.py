from flask import Flask, jsonify, render_template

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/todolist", methods=["GET"])
def api_todolist_get():
    d = []
    return jsonify(d)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)
