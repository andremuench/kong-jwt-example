from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route("/hello")
def hello():
    return jsonify({"message":"Hello"}), 200


@app.route("/secret")
def secret():
    return jsonify({"message":"This is a kong secured route"}), 200


if __name__ == '__main__':
    app.run()
