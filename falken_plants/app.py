# by Richi Rod AKA @richionline / falken20
# ./falken_teleworking/__init__.py

from flask import Flask
import os
from dotenv import load_dotenv, find_dotenv
from flask_login import LoginManager
import pprint

from .logger import Log, console
from .config import get_settings, print_app_config, print_settings_environment
from .cache import check_cache
from .models import db

Log.debug("Loading app.py")

# Set environment vars
load_dotenv(find_dotenv())
settings = get_settings()
Log.debug(f"Settings: {settings}")
# pprint.pprint(settings.dict())

console.rule(settings.APP_DATA['title'] + " " +
             settings.APP_DATA['version'] + " by " + settings.APP_DATA['author'])

# Cache info
check_cache()

basedir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def create_app(config_mode="development"):
    app = Flask(__name__, template_folder="../templates",
                static_folder="../static")
    # print_settings_environment(settings)

    app.config.from_object(settings)
    app.config.from_object(settings.CONFIG_ENV[config_mode])

    app.config['TEMPLATE_AUTO_RELOAD'] = True
    app.config['DEBUG'] = True if config_mode == "development" else False

    Log.info(
        f"***************** Running in {config_mode.upper()} mode *****************", style="red bold")

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

    # blueprint for API urls
    from .urls import urls as urls_blueprint
    app.register_blueprint(urls_blueprint)

    # blueprint for swagger
    from .swagger import swagger_ui_blueprint, SWAGGER_URL
    app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)
    Log.debug(f"Running Swagger in {SWAGGER_URL}")

    if config_mode == "testing":
        print_settings_environment(settings.CONFIG_ENV["testing"])
    else:
        print_app_config(app)

    return app


# If FLASK_DEBUG is True, the reloader will be enabled by default and the thread starts twice.
Log.info("Creating app...")
app = create_app(config_mode=settings.CONFIG_MODE)
