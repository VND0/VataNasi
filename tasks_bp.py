from flask import redirect, Blueprint, render_template, request
from flask_login import current_user

import funcs
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
    if mode != 1:
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
            return redirect(
                f"/task/{mode}?ic={int(instant_check)}{''.join(f'&cat={c}' for c in chosen_categories)}&amount={amount}"
            )

    return render_template("mode_preferences_page.html", is_authenticated=current_user.is_authenticated, **kwargs)




@bp.route("/task/1", methods=["POST", "GET"])
def typing_mode():
    if not current_user.is_authenticated:
        redirect("/")

    data = funcs.parse_task1_args(request.args)
    words = set()
    for c in data.categories:
        words_objects = db.get_words_objects(current_user.id, c)
        for w in words_objects:
            words.add((w.value, w.translation))
    words = list(words)[:(data.words_amount if data.words_amount else len(words))]

    values = [w[0] for w in words]
    translations = [w[1].lower() for w in words]

    if request.method == "POST":
        success = []
        mistakes = []
        for v, t in zip(values, translations):
            v_got = request.form.get(v)
            t_got = request.form.get(f"{v}-translation")

            if t_got is None:
                mistakes.append((v_got, "", translations[values.index(v_got)]))
            elif t_got.lower() == translations[values.index(v_got)]:
                success.append(v_got)
            else:
                mistakes.append((v_got, t_got, translations[values.index(v_got)]))

        return render_template("result_page.html", is_authenticated=current_user.is_authenticated,
                               correct_answers=success, wrong_answers=mistakes)

    return render_template("typing_mode_page.html", is_authenticated=current_user.is_authenticated,
                           values=values)
