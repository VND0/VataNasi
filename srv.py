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
def load_user(id: int):
    return db.select_user_by_id(id)


@app.route("/")
def handle_main_page():
    bs_css = url_for('static', filename='bootstrap/bootstrap.min.css')
    bs_js = url_for('static', filename='bootstrap/bootstrap.bundle.min.js')
    script_js = url_for('static', filename='script.js')
    return render_template("index.html", bs_css=bs_css, bs_js=bs_js, script_js=script_js)


@app.route("/register", methods=["POST", "GET"])
def handle_register_page():
    if current_user.is_authenticated:
        return redirect("/")

    bs_css = url_for('static', filename='bootstrap/bootstrap.min.css')
    bs_js = url_for('static', filename='bootstrap/bootstrap.bundle.min.js')
    script_js = url_for('static', filename='script.js')

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        password_confirm = request.form.get("password_confirm")

        if not username.isalnum():
            message = "Имя пользователя содержит недопустимые символы."
            return render_template("reg_page.html", bs_css=bs_css, bs_js=bs_js, script_js=script_js,
                                   add_message=True, type="warning", message=message)
        elif password != password_confirm:
            message = "Пароли не совпадают"
            return render_template("reg_page.html", bs_css=bs_css, bs_js=bs_js, script_js=script_js,
                                   add_message=True, type="warning", message=message)
        elif not db.is_username_new(username):
            message = "Имя пользователя занято."
            return render_template("reg_page.html", bs_css=bs_css, bs_js=bs_js, script_js=script_js,
                                   add_message=True, type="warning", message=message)
        try:
            db.new_user(username, passd_to_hash(password))
        except Exception as e:
            print(e)
            message = "Внутренняя ошибка сервера."
            return render_template("reg_page.html", bs_css=bs_css, bs_js=bs_js, script_js=script_js,
                                   add_message=True, type="danger", message=message)

        message = f"Пользователь {username} успешно добавлен."
        return render_template("reg_page.html", bs_css=bs_css, bs_js=bs_js, script_js=script_js,
                               add_message=True, type="success", message=message)

    return render_template("reg_page.html", bs_css=bs_css, bs_js=bs_js, script_js=script_js, add_message=False)


@app.route("/login", methods=["GET", "POST"])
def handle_login_page():
    if current_user.is_authenticated:
        return redirect("/")

    bs_css = url_for('static', filename='bootstrap/bootstrap.min.css')
    bs_js = url_for('static', filename='bootstrap/bootstrap.bundle.min.js')
    script_js = url_for('static', filename='script.js')

    for_auth_js = url_for("static", filename="for_auth.js")

    if request.method == "POST":
        username = request.form.get("username").strip()
        password = request.form.get("password").strip()
        password_hash = passd_to_hash(password)

        if not username:
            return render_template("auth_page.html", bs_css=bs_css, bs_js=bs_js, script_js=script_js, add_message=True,
                                   for_auth_js=for_auth_js, type="warning", message="Поле логина пустое")
        if not password:
            return render_template("auth_page.html", bs_css=bs_css, bs_js=bs_js, script_js=script_js, add_message=True,
                                   for_auth_js=for_auth_js, type="warning", message="Поле пароля пустое")

        user = db.get_user(username, password_hash)
        if user is None:
            return render_template("auth_page.html", bs_css=bs_css, bs_js=bs_js, script_js=script_js, add_message=True,
                                   for_auth_js=for_auth_js, type="warning",
                                   message="Неверные имя пользователя или пароль.")
        login_user(user)

    return render_template("auth_page.html", bs_css=bs_css, bs_js=bs_js, script_js=script_js, for_auth_js=for_auth_js,
                           add_message=False)


@app.route("/check")
def check_login():
    if current_user.is_authenticated:
        return "Logged in"
    return "Logged out"


@login_required
@app.route("/logout")
def logout():
    logout_user()
    return redirect("/")


if __name__ == '__main__':
    with open("secret_key.txt", "r") as f:
        key = f.read()
        app.config["SECRET_KEY"] = key
    db.create_tables_if_not_exist()
    app.run(port=8000, host="0.0.0.0")
