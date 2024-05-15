from flask import redirect, Blueprint, render_template
from flask_login import current_user

from db.interfaces import DataBase

bp = Blueprint("my_words", __name__)
db = DataBase("data.db")


@bp.route("/my_words")
def my_words_page():
    if not current_user.is_authenticated:
        return redirect("/login")

    return render_template("words_list_page.html",
                           categories=db.get_categories_of_user(current_user.id))
    # categories=[])
