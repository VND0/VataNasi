import hashlib

from flask import Flask, render_template, url_for, request, redirect
from flask_login import LoginManager, login_user, current_user, login_required, logout_user

from db.interfaces import DataBase

app = Flask(__name__)
db = DataBase("data.db")
login_manager = LoginManager(app)


def passd_to_hash(password: str) -> str:
    return hashlib.md5(password.encode("utf-8")).hexdigest()


@login_manager.user_loader
def load_user(user_id: int):
    return db.select_user_by_id(user_id)


@app.route("/")
def handle_main_page():
    return render_template("index.html", is_authenticated=current_user.is_authenticated)


@app.route("/register", methods=["POST", "GET"])
def handle_register_page():
    if current_user.is_authenticated:
        return redirect("/")

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        password_confirm = request.form.get("password_confirm")
        password_hash = passd_to_hash(password)

        if not username.isalnum():
            message = "Имя пользователя содержит недопустимые символы."
            return render_template("reg_page.html", add_message=True, type="warning", message=message,
                                   is_authenticated=current_user.is_authenticated)
        elif password != password_confirm:
            message = "Пароли не совпадают"
            return render_template("reg_page.html", add_message=True, type="warning", message=message,
                                   is_authenticated=current_user.is_authenticated)
        elif not db.is_username_new(username):
            message = "Имя пользователя занято."
            return render_template("reg_page.html", add_message=True, type="warning", message=message,
                                   is_authenticated=current_user.is_authenticated)
        try:
            db.new_user(username, password_hash)
        except Exception as e:
            print(e)
            message = "Внутренняя ошибка сервера."
            return render_template("reg_page.html", add_message=True, type="danger", message=message,
                                   is_authenticated=current_user.is_authenticated)

        added_user = db.get_user(username, password_hash)  # Здесь пользователь гарантированно существует.
        login_user(added_user)  # TODO: оптимизировать двойной запрос
        return redirect("/")

    return render_template("reg_page.html", add_message=False,
                           is_authenticated=current_user.is_authenticated)


@app.route("/login", methods=["GET", "POST"])
def handle_login_page():
    if current_user.is_authenticated:
        return redirect("/")

    if request.method == "POST":
        username = request.form.get("username").strip()
        password = request.form.get("password").strip()
        password_hash = passd_to_hash(password)

        if not username:
            return render_template("auth_page.html", add_message=True, type="warning",
                                   message="Поле логина пустое", is_authenticated=current_user.is_authenticated)
        if not password:
            return render_template("auth_page.html", add_message=True, type="warning",
                                   message="Поле пароля пустое", is_authenticated=current_user.is_authenticated)

        user = db.get_user(username, password_hash)
        if user is None:
            return render_template("auth_page.html", add_message=True, type="warning",
                                   message="Неверные имя пользователя или пароль.",
                                   is_authenticated=current_user.is_authenticated)
        login_user(user)
        return redirect("/")

    return render_template("auth_page.html", add_message=False,
                           is_authenticated=current_user.is_authenticated)


@login_required
@app.route("/logout")
def logout():
    logout_user()
    return redirect("/")


@app.route("/my_words")
def my_words_page():
    if not current_user.is_authenticated:
        return redirect("/login")

    raise NotImplementedError


@app.route("/new_task")
def new_task_page():
    if not current_user.is_authenticated:
        return redirect("/login")

    raise NotImplementedError


@login_required
@app.route("/change_account_data")
def change_account_data_page():
    if not current_user.is_authenticated:
        return redirect("/")

    if request.method == "POST":
        pass

    return render_template("change_account_data.html", add_message=False)


if __name__ == '__main__':
    with open("secret_key.txt", "r") as f:
        key = f.read()
        app.config["SECRET_KEY"] = key
    db.create_tables_if_not_exist()
    app.run(port=8000, host="0.0.0.0")
