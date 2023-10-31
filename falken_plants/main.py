# by Richi Rod AKA @richionline / falken20
# ./falken_plants/main.py

from flask import Blueprint, render_template
from flask_login import login_required, current_user

from .logger import Log

main = Blueprint('main', __name__)


@main.route("/", methods=('GET', 'POST'))
@main.route("/home", methods=('GET', 'POST'))
@login_required
def index():
    Log.info("Index page")
    Log.debug(f"Current user: {current_user}")

    return render_template('index.html')


@main.route("/profile", methods=['GET'])
@login_required
def profile():
    Log.info("Profile page")
    Log.debug(f"Current user: {current_user}")

    return render_template('profile.html', name=current_user.name, date_from=current_user.date_from)


@main.route("/search", methods=['GET', 'POST'])
@login_required
def search():
    Log.info("Search page")
    Log.debug(f"Current user: {current_user}")

    pass


@main.route("/calendar", methods=['GET'])
@login_required
def calendar():
    Log.info("Calendar page")
    Log.debug(f"Current user: {current_user}")

    return render_template('calendar.html')
