from flask import Flask, render_template
from flask_migrate import Migrate

from config import Config

app = Flask(__name__)
app.config.from_object(Config)

with app.app_context():
    from .auth.authservice import google_blueprint, login_manager
    from .auth.models import User, OAuth, db
    from .auth import auth_blueprint

    app.register_blueprint(auth_blueprint, url_prefix="/auth")


db.init_app(app)
login_manager.init_app(app)
migrate = Migrate(app, db)


@app.route("/")
def index():
    return render_template("home.jinja2")
