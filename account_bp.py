from flask import Blueprint, request, render_template, redirect
from flask_login import current_user, login_user, login_required, logout_user

from db.interfaces import DataBase
from funcs import passd_to_hash

bp = Blueprint("account", __name__)
db = DataBase("data.db")


@bp.route("/register", methods=["POST", "GET"])
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


@bp.route("/login", methods=["GET", "POST"])
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
@bp.route("/logout")
def logout():
    logout_user()
    return redirect("/")


@login_required
@bp.route("/change_account_data")
def change_account_data_page():
    if not current_user.is_authenticated:
        return redirect("/")

    if request.method == "POST":
        pass

    return render_template("change_account_data.html", add_message=False)
