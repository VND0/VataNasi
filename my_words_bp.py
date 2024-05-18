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


def handle_add_new_form() -> dict:
    new_name = request.form.get("new-category-name")
    user_id = current_user.id
    response = db.new_category(user_id, new_name)
    return {"message": response}


@bp.route("/my_words", methods=["POST", "GET"])
def my_words_page():
    if not current_user.is_authenticated:
        return redirect("/login")

    kwargs = {}
    if request.method == "POST":
        if not (request.form.get("new-category-name") is None):
            kwargs = handle_add_new_form()
        else:
            raise NotImplementedError

        if not kwargs["message"]:
            return redirect("/my_words")

    return render_template("categories_list_page.html", is_authenticated=current_user.is_authenticated, **kwargs,
                           categories=db.get_categories_of_user(current_user.id))
    # TODO: пофиксить вообще все
    # categories=[])
