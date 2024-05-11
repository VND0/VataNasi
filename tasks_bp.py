from flask import redirect, Blueprint
from flask_login import current_user

bp = Blueprint("tasks", __name__)


@bp.route("/new_task")
def new_task_page():
    if not current_user.is_authenticated:
        return redirect("/login")

    raise NotImplementedError
