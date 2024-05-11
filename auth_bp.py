from flask import request, render_template, redirect, Blueprint
from flask_login import current_user, login_user, logout_user, login_required

from db.interfaces import DataBase
from funcs import passd_to_hash

bp = Blueprint("authorization", __name__)
db = DataBase("data.db")


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
