from flask import Blueprint, flash, redirect, url_for
from flask_login import login_required, logout_user

auth_blueprint = Blueprint("auth", __name__)


@auth_blueprint.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have logged out")
    return redirect(url_for("index"))
