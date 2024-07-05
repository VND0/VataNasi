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
        elif not password.strip():
            message = "Пустой пароль"
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

        added_user = db.get_user_by_username(username, password_hash)  # Здесь пользователь гарантированно существует.
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

        user = db.get_user_by_username(username, password_hash)
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
@bp.route("/change_account_data", methods=["POST", "GET"])
def change_account_data_page():
    if not current_user.is_authenticated:
        return redirect("/")

    additional_kwargs = {"add_message": False}
    if request.method == "POST":
        additional_kwargs["add_message"] = True
        # На странице две формы. Код ниже определяет, какая именно была отправлена.
        if request.form.get("old-password") is None:
            password = request.form.get("password")
            if passd_to_hash(password) == current_user.password_hash:
                remembered = current_user.username
                logout_user()
                db.delete_user(remembered)
                return redirect("/")
            else:
                additional_kwargs["type"] = "warning"
                additional_kwargs["message"] = "Неправильный пароль"
        else:
            old = request.form.get("old-password")
            new = request.form.get("new-password")

            if current_user.password_hash != passd_to_hash(old):
                additional_kwargs["type"] = "warning"
                additional_kwargs["message"] = "Неправильный старый пароль"
            elif not new:
                additional_kwargs["type"] = "warning"
                additional_kwargs["message"] = "Пустой новый пароль"
            else:
                new_password_hash = passd_to_hash(new)
                db.change_passwd(current_user.username, new_password_hash)
                additional_kwargs["type"] = "success"
                additional_kwargs["message"] = "Пароль успешно обновлен"

    return render_template("edit_account.html", current_username=current_user.username, **additional_kwargs,
                           is_authenticated=current_user.is_authenticated)
