# by Richi Rod AKA @richionline / falken20
# ./falken_plants/main.py

from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from datetime import date
import sys

from .logger import Log
from .controllers import ControllerPlant
from . import urls

main = Blueprint('main', __name__)


@main.route("/", methods=('GET', 'POST'))
@main.route("/home", methods=('GET', 'POST'))
@login_required
def index():
    Log.info("Index page")
    Log.debug(f"Current user: {current_user}")

    all_plants = ControllerPlant.get_all_plants(current_user.id)

    # return redirect(url_for('main.view_all_plants'))
    return render_template('plant_list.html', plants=all_plants, message="")


@main.route('/show_grouped/')
@login_required
def show_grouped():
    Log.info("Show grouped page")
    Log.debug(f"Current user: {current_user}")

    all_plants = ControllerPlant.get_all_plants(current_user.id)

    return render_template('plant_list_group.html', plants=all_plants, message="")


@main.route("/profile", methods=['GET'])
@login_required
def profile():
    Log.info("Profile page")
    Log.debug(f"Current user: {current_user}")

    return render_template('profile.html', name=current_user.name, date_created=current_user.date_created)


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


