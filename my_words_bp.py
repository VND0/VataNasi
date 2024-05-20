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


@bp.route("/del-word", methods=["POST"])
def del_word():
    data = request.get_json()
    category_name = data["category"]
    word = data["word"]
    db.del_word(current_user.id, category_name, word)
    return ""


def handle_add_new_category_form() -> dict:
    new_name = request.form.get("new-category-name")
    if not new_name:
        return {"message": "Имя категории не может быть пустым."}
    elif "/" in new_name:
        return {"message": "Нельзя использовать знак '/' в названии категории."}
    user_id = current_user.id
    response = db.new_category(user_id, new_name)
    return {"message": response}


@bp.route("/my_categories", methods=["POST", "GET"])
def my_categories_page():
    if not current_user.is_authenticated:
        return redirect("/login")

    kwargs = {}
    if request.method == "POST":
        if not (request.form.get("new-category-name") is None):
            kwargs = handle_add_new_category_form()
        else:
            raise NotImplementedError

        if not kwargs["message"]:
            return redirect("/my_categories")

    return render_template("categories_list_page.html", is_authenticated=current_user.is_authenticated, **kwargs,
                           categories=db.get_categories_of_user(current_user.id))


@bp.route("/my_words/<category>", methods=["POST", "GET"])
def my_words_page(category: str):
    if not current_user.is_authenticated:
        return redirect("/login")
    kwargs = {"category": category}

    if request.method == "POST":
        value = request.form.get("value")
        translation = request.form.get("translation")
        if not (value and translation):
            kwargs["message"] = "Поля не должны быть пусты"
        else:
            try:
                db.new_word(current_user.id, category, value, translation)
            except ValueError as e:
                kwargs["message"] = str(e)

    try:
        words_reprs = db.get_words_of_category(category, current_user.id)
        kwargs["words"] = words_reprs
    except ValueError as e:
        kwargs["message"] = str(e)

    return render_template("words_list_page.html", is_authenticated=current_user.is_authenticated, **kwargs,
                           current_category=category)
