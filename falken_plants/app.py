# by Richi Rod AKA @richionline / falken20
# ./falken_teleworking/__init__.py

from flask import Flask
import os
from dotenv import load_dotenv, find_dotenv
from flask_login import LoginManager

from .logger import Log, console
from .config import get_settings, print_app_config
from .cache import check_cache
from .models import db

# Set environment vars
load_dotenv(find_dotenv())
settings = get_settings()

console.rule(settings.APP_DATA['title'] + " " +
             settings.APP_DATA['version'] + " by " + settings.APP_DATA['author'])

# Cache info
check_cache()

basedir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# TODO: Review how to init config_mode parameter
def create_app(config_mode='development'):
    app = Flask(__name__, template_folder="../templates",
                static_folder="../static")

    Log.info(f"Running in {config_mode} mode", style="red bold")
    Log.info(f"Config mode: {app.config['DEBUG']}", style="red bold")

    app.config.from_object(settings)
    app.config.from_object(settings.CONFIG_ENV[config_mode])

    app.config['TEMPLATE_AUTO_RELOAD'] = True

    """
    if settings.ENV_PRO == "N":
        # basedir is the path to the root of the project
        Log.info(
            f"DB path: {os.path.join(basedir, 'database.db')}", style="red bold")
        app.config['DEBUG'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
            os.path.join(basedir, 'database.db')
    else:
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL'].replace(
            "://", "ql://", 1)
    """

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

    print_app_config(app)

    return app


app = create_app(config_mode='development')