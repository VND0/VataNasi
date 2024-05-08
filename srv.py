from flask import Flask, render_template, url_for, request
import hashlib
from db.interfaces import DataBase
from flask_login import LoginManager, login_user, current_user, logout_user

app = Flask(__name__)
db = DataBase("data.db")
login_manager = LoginManager(app)


def passd_to_hash(password: str) -> str:
    return hashlib.md5(password.encode("utf-8")).hexdigest()


@app.route("/")
def handle_main_page():
    bs_css = url_for('static', filename='bootstrap/bootstrap.min.css')
    bs_js = url_for('static', filename='bootstrap/bootstrap.bundle.min.js')
    script_js = url_for('static', filename='script.js')
    return render_template("index.html", bs_css=bs_css, bs_js=bs_js, script_js=script_js)


@app.route("/register", methods=["POST", "GET"])
def handle_register_page():
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


@app.route("/login")
def handle_login_page():
    bs_css = url_for('static', filename='bootstrap/bootstrap.min.css')
    bs_js = url_for('static', filename='bootstrap/bootstrap.bundle.min.js')
    script_js = url_for('static', filename='script.js')

    for_auth_js = url_for("static", filename="for_auth.js")

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        password_hash = passd_to_hash(password)

    return render_template("auth_page.html", bs_css=bs_css, bs_js=bs_js, script_js=script_js, for_auth_js=for_auth_js)


if __name__ == '__main__':
    db.create_tables_if_not_exist()
    app.run(port=8000, host="0.0.0.0")
