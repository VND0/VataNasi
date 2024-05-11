from flask import request, render_template, redirect, Blueprint
from flask_login import current_user, login_required

bp = Blueprint("edit_account_data", __name__)


@login_required
@bp.route("/change_account_data")
def change_account_data_page():
    if not current_user.is_authenticated:
        return redirect("/")

    if request.method == "POST":
        pass

    return render_template("change_account_data.html", add_message=False)
