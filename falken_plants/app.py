# by Richi Rod AKA @richionline / falken20
# ./falken_teleworking/__init__.py

from flask import Flask
import os
from dotenv import load_dotenv, find_dotenv
from flask_login import LoginManager

from .logger import Log, console
from .config import get_settings
from .cache import check_cache
from .models import db

# Set environment vars
load_dotenv(find_dotenv())
settings = get_settings()

console.rule(settings.SETUP_DATA['title'] + " " +
             settings.SETUP_DATA['version'] + " by " + settings.SETUP_DATA['author'])

# Cache info
check_cache()

basedir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

from .config import config
# TODO: Review config file


def create_app():
    app = Flask(__name__, template_folder="../templates",
                static_folder="../static")

    app.config['SECRET_KEY'] = os.getenv(
        'SECRET_KEY', 'your-special-secret-key')
    app.config['TEMPLATE_AUTO_RELOAD'] = True

    if settings.ENV_PRO == "N":
        # basedir is the path to the root of the project
        Log.info("Running in development mode with Sqlite DB", style="red bold")
        Log.info(
            f"DB path: {os.path.join(basedir, 'database.db')}", style="red bold")
        app.config['DEBUG'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
            os.path.join(basedir, 'database.db')
    else:
        Log.info("Running in production mode with postgres DB", style="red")
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL'].replace(
            "://", "ql://", 1)

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    db.init_app(app)

    # A user loader tells Flask-Login how to find a specific user from the ID that is stored in their
    # session cookie.
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        # Since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # blueprint for swagger
    from .swagger import swagger_ui_blueprint, SWAGGER_URL
    app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)
    Log.debug(f"Running Swagger in {SWAGGER_URL}")

    return app
