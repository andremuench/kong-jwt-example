from flask import Flask, request, jsonify
import os
from jwcrypto import jwt, jwk
from exception import UnauthorizedError, ClientException

ADMIN_USER = os.environ.get("ADMIN_USER", "admin")
ADMIN_PWD = os.environ.get("ADMIN_PASSWORD", "admin")

PRIVATE_PEM_PATH = os.environ.get("PRIVATE_PEM_PATH")
ISSUER = os.environ.get("AUTH_ISSUER", "kong-auth")

if not PRIVATE_PEM_PATH:
    raise Exception("Pem path not given via PRIVATE_PEM_PATH variable")

if not os.path.exists(PRIVATE_PEM_PATH):
    raise Exception(f"path to private pem not set or incorrect: {PRIVATE_PEM_PATH}")

with open(PRIVATE_PEM_PATH, 'rb') as key_file:
    key_data = key_file.read()
    jwt_key = jwk.JWK.from_pem(key_data)

app = Flask(__name__)


@app.errorhandler(UnauthorizedError)
def unauthorized_error(exception):
    return "", 401


@app.errorhandler(ClientException)
def client_error(exception):
    return "", 400


@app.route("/auth", methods=["POST"])
def auth():
    try:
        user = request.form["user"]
        pwd = request.form["password"]
    except KeyError:
        raise ClientException

    if user != ADMIN_USER or pwd != ADMIN_PWD:
        raise UnauthorizedError

    for_user = request.form.get("user-for")
    return jsonify({"access_token": make_signed_token(_for=for_user)})


def make_signed_token(_for=None):
    header = {"alg": "RS256", "typ": "JWT"}
    claims = {"iss": ISSUER}
    if _for:
        claims["user"] = _for
    token = jwt.JWT(header=header, claims=claims, default_claims={"iat": None, "exp": None})
    token.make_signed_token(jwt_key)
    return token.serialize()


if __name__ == '__main__':
    app.run()
