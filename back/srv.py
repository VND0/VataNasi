import hashlib

from flask import Flask, request
from flask_cors import CORS

from db.interfaces import DataBase

app = Flask(__name__)
CORS(app)
db = DataBase("data.db")


def passd_to_hash(password: str) -> str:
    return hashlib.md5(password.encode("utf-8")).hexdigest()


@app.route("/check_unique_uname/<username>", methods=["GET"])
def check_uname_handler(username: str):
    result = db.check_unique_username(username)
    return str(int(result))


@app.route("/reg", methods=["POST"])
def registration_handler():
    # TODO: кибербезопасность стремится к нулю
    args = request.get_json()
    username = args.get("username")
    password = args.get("password")
    if username is None or password is None:
        return "Логин или пароль не содержится в отправлении на сервер.", 400
    if not check_uname_handler(username):  # TODO: мб стоит удрать проверку
        return "Логин занят.", 400

    try:
        db.new_user(username, passd_to_hash(password))
    except Exception as e:
        return str(e), 500
    return f"Пользователь {username} добавлен."


if __name__ == '__main__':
    db.create_tables_if_not_exist()
    app.run(debug=False, host="0.0.0.0", port=8001)
