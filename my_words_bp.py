from flask import redirect, Blueprint
from flask_login import current_user

bp = Blueprint("my_words", __name__)


@bp.route("/my_words")
def my_words_page():
    if not current_user.is_authenticated:
        return redirect("/login")

    raise NotImplementedError
