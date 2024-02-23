# by Richi Rod AKA @richionline / falken20
# ./falken_plants/main.py

from flask import Blueprint, render_template
from flask_login import login_required, current_user
from datetime import date
from flask import request
import sys

from .logger import Log
from .controllers import ControllerPlant

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


# ###### API plants ######

@main.route("/plants/create", methods=['GET'])
@login_required
def create_plant():
    Log.info("Create plant page")
    Log.debug(f"Current user: {current_user}")

    return render_template('plant_form.html')


@main.route("/plants", methods=['GET'])
@login_required
def view_all_plants():
    Log.info("View all the plants page")
    Log.debug(f"Current user: {current_user}")

    # return render_template('add_plant.html')


@main.route("/plants/<int:plant_id>", methods=['GET'])
@login_required
def view_plant(plant_id: int):
    Log.info("View plant page")
    Log.debug(f"Current user: {current_user}")

    pass


@main.route("/plants", methods=['POST'])
@login_required
def add_plant():
    Log.info("Add plant page")
    Log.debug(f"Current user: {current_user}")

    try:
        Log.debug(f"Request form: {request.form}")
        plant = ControllerPlant.create_plant(name=request.form['name'],
                                             name_tech=request.form['name_tech'],
                                             comment=request.form['comment'],
                                             watering_summer=request.form['watering_summer'],
                                             watering_winter=request.form['watering_winter'],
                                             spray=request.form['spray'],
                                             direct_sun=request.form['direct_sun'],
                                             image=request.form['image'],
                                             user_id=current_user.id)
        Log.info(f"Plant created: {plant}")
    except Exception as e:
        Log.error("Error creating plant", err=e, sys=sys)
        return render_template('plant_form.html', error=e)

    return render_template('index.html')


@main.route("/plants/<int:plant_id>", methods=['PUT'])
@login_required
def update_plant(plant_id: int):
    Log.info("Update plant page")
    Log.debug(f"Current user: {current_user}")

    pass


@main.route("/plants/<int:plant_id>", methods=['DELETE'])
@login_required
def delete_plant(plant_id: int):
    Log.info("Delete plant page")
    Log.debug(f"Current user: {current_user}")

    pass


@main.route("/plants/<int:plant_id>/calendar/water", methods=['POST'])
@login_required
def water_plant(plant_id: int):
    Log.info("Water plant page")
    Log.debug(f"Current user: {current_user}")

    pass


@main.route("/plants/<int:plant_id>/calendar/fertilize", methods=['POST'])
@login_required
def fertilize_plant(plant_id: int):
    Log.info("Fertilize plant page")
    Log.debug(f"Current user: {current_user}")

    pass


@main.route("/plants/<int:plant_id>/calendar", methods=['GET'])
@login_required
def view_calendar(plant_id: int):
    Log.info("View calendar page")
    Log.debug(f"Current user: {current_user}")

    pass


@main.route("/plants/<int:plant_id>/calendar/<date>", methods=['GET'])
@login_required
def view_calendar_date(plant_id: int, date_calendar: date):
    Log.info("View calendar date page")
    Log.debug(f"Current user: {current_user}")

    pass


@main.route("/plants/<int:plant_id>/calendar/<date>", methods=['POST'])
@login_required
def add_calendar_date(plant_id: int, date_calendar: date):
    Log.info("Add calendar date page")
    Log.debug(f"Current user: {current_user}")

    pass


@main.route("/plants/<int:plant_id>/calendar/<date>", methods=['PUT'])
@login_required
def update_calendar_date(plant_id: int, date_calendar: date):
    Log.info("Update calendar date page")
    Log.debug(f"Current user: {current_user}")

    pass
