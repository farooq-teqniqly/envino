from datetime import datetime

from flask_dance.consumer import oauth_authorized, oauth_error
from flask_dance.consumer.storage.sqla import SQLAlchemyStorage
from flask_dance.contrib.google import make_google_blueprint
from flask_login import LoginManager, current_user, login_user
from flask import current_app, flash
from sqlalchemy.orm.exc import NoResultFound

from .models import User, OAuth, db
from .. import app

google_blueprint = make_google_blueprint(
    client_id=current_app.config["GOOGLE_CLIENT_ID"],
    client_secret=current_app.config["GOOGLE_CLIENT_SECRET"],
    scope=["profile", "email"],
)

google_blueprint.backend = SQLAlchemyStorage(OAuth, db.session, user=current_user)

app.register_blueprint(google_blueprint, url_prefix="/login")

login_manager = LoginManager()
login_manager.login_view = "google.login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@oauth_authorized.connect_via(google_blueprint)
def google_logged_in(blueprint, token):
    if not token:
        flash("Failed to log in with {name}".format(name=blueprint.name))
        return
    # figure out who the user is
    resp = blueprint.session.get("/oauth2/v1/userinfo")
    if resp.ok:
        resp_json = resp.json()
        username = resp_json["email"]
        email = username
        query = User.query.filter_by(username=username, email=email, is_authorized=1)
        try:
            authorized_user = query.one()

            token_model = OAuth(
                user_id=authorized_user.id,
                token=token["id_token"],
                access_token=token["access_token"],
                expires_in=datetime.utcfromtimestamp(int(token["expires_at"])),
            )

            db.session.add(token_model)

            try:
                db.session.commit()
                login_user(authorized_user)
                flash("Successfully signed in with Google")
            except Exception:
                db.session.rollback()
                flash("Could not add token to database.")
            finally:
                db.session.close()

        except NoResultFound:
            msg = "You are not authorized to use this application. Please request access from the administrator."
            flash(msg, category="error")
    else:
        msg = "Failed to fetch user info from {name}".format(name=blueprint.name)
        flash(msg, category="error")


@oauth_error.connect_via(google_blueprint)
def google_error(blueprint, error, error_description=None, error_uri=None):
    msg = (
        "OAuth error from {name}! " "error={error} description={description} uri={uri}"
    ).format(
        name=blueprint.name, error=error, description=error_description, uri=error_uri,
    )
    flash(msg, category="error")
