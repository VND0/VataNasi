from flask import redirect, Blueprint, render_template, request
from flask_login import current_user

from db.interfaces import DataBase

bp = Blueprint("tasks", __name__)
db = DataBase("data.db")


@bp.route("/new_task")
def new_task_page():
    if not current_user.is_authenticated:
        return redirect("/login")

    return render_template("choose_tasks_page.html", is_authenticated=current_user.is_authenticated)


@bp.route("/task-preferences/<int:mode>", methods=["POST", "GET"])
def preferences_page(mode: int):
    if not current_user.is_authenticated:
        return redirect("/login")
    if mode != 0:
        return redirect("/new_task")

    categories_names = db.get_categories_of_user(current_user.id)
    kwargs = {"categories": categories_names}
    if request.method == "POST":
        instant_check = request.form.get("check_type") == "on"
        chosen_categories = [c for c in categories_names if request.form.get(c) == "on"]
        amount_raw = request.form.get("amount")

        if instant_check:
            kwargs["message"] = "Моментальная проверка в разработке"
        elif not chosen_categories:
            kwargs["message"] = "Не выбраны категории"
        elif amount_raw and (amount_raw[0] in ("0", "-") or not amount_raw.isdigit()):
            kwargs["message"] = "Неверный формат введенного числа"
        else:
            amount = 0 if not amount_raw else int(amount_raw)
            return redirect(f"/task/{mode}/{int(instant_check)}/{'/'.join(chosen_categories)}/{amount}")

    return render_template("mode_preferences_page.html", is_authenticated=current_user.is_authenticated, **kwargs)
