from flask import Flask, render_template
from flask_login import LoginManager, current_user

import account_bp
import my_words_bp
import tasks_bp
from db.interfaces import DataBase

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
db = DataBase("data.db")
login_manager = LoginManager(app)


@login_manager.user_loader
def load_user(user_id: int):
    return db.get_user_by_id(user_id)


@app.route("/")
def handle_main_page():
    return render_template("index.html", is_authenticated=current_user.is_authenticated)


if __name__ == '__main__':
    with open("secret_key.txt", "r") as f:
        key = f.read()
        app.config["SECRET_KEY"] = key

    app.register_blueprint(account_bp.bp)
    app.register_blueprint(my_words_bp.bp)
    app.register_blueprint(tasks_bp.bp)

    db.create_tables_if_not_exist()
    app.run(port=80, host="0.0.0.0")
