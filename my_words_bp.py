from flask import redirect, Blueprint, render_template, request
from flask_login import current_user, login_required

from db.interfaces import DataBase

bp = Blueprint("my_words", __name__)
db = DataBase("data.db")


@login_required
@bp.route("/del-category", methods=["POST"])
def del_category():
    category_name = request.get_json()
    db.delete_category(current_user.id, category_name["category_name"])
    return ""


@bp.route("/my_words")
def my_words_page():
    if not current_user.is_authenticated:
        return redirect("/login")

    return render_template("categories_list_page.html", is_authenticated=current_user.is_authenticated,
                           categories=db.get_categories_of_user(current_user.id))
    # categories=[])
