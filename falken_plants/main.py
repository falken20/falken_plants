# by Richi Rod AKA @richionline / falken20
# ./falken_plants/main.py

from flask import Blueprint, render_template
from flask_login import login_required, current_user
from datetime import date
from flask import request, redirect, url_for
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


# ###### API plants ######

@main.route("/plants", methods=['GET'])
@login_required
def view_all_plants():
    Log.info("View all the plants page")
    Log.info(f"Method: {request.method}")
    Log.debug(f"Current user: {current_user}")

    all_plants = ControllerPlant.get_all_plants(current_user.id)

    return render_template('plant_list.html', plants=all_plants, message="")


@main.route("/plants/create", methods=['GET'])
@login_required
def create_plant():
    Log.info("Create plant page")
    Log.info(f"Method: {request.method}")
    Log.debug(f"Current user: {current_user}")

    return render_template('plant_form.html', plant=None, form_method="POST")


@main.route("/plants/update/<int:plant_id>", methods=['GET'])
@login_required
def update_plant(plant_id: int):
    Log.info("Edit plant page")
    Log.info(f"Method: {request.method}")
    Log.debug(f"Current user: {current_user}")

    plant = ControllerPlant.get_plant(plant_id)
    Log.debug(f"Plant to update: {plant}")

    return render_template('plant_form.html', plant=plant, form_method="PUT")


# TODO: Make it work and make form read_only
@main.route("/plants/<int:plant_id>", methods=['GET'])
@login_required
def view_plant(plant_id: int):
    Log.info("View plant page")
    Log.info(f"Method: {request.method}")
    Log.debug(f"Current user: {current_user}")

    plant = ControllerPlant.get_plant(plant_id)
    Log.debug(f"Plant to view: {plant}")

    return render_template('plant_form.html', plant=plant, form_method="GET")


@main.route("/plants", methods=['POST'])
@login_required
def post_plant():
    # Because HTML doesn't support PUT method, we use a hidden field to know if its a PUT method
    Log.info("Add or update plant API")
    Log.info(f"Method: {request.method}")
    Log.info(f"Hidden Method: {request.form['_method']}")
    Log.debug(f"Current user: {current_user}")

    try:
        Log.debug(f"Request form: {request.form}")
        # Because HTML doesn't support PUT method, we use a hidden field to know if its a PUT method
        if request.form['_method'] == "PUT":
            Log.info(
                f"Its a PUT method, redirect to update plant API: /plants/{request.form['id']}")
            # return redirect(f"/plants/{request.form['id']}")
            # return redirect(url_for('main.put_plant', plant_id=request.form['id'], method='PUT'))
            # put_plant(request.form['id'])

            plant_id = request.form['id']
            plant = ControllerPlant.update_plant(plant_id=plant_id,
                                                 name=request.form['name'],
                                                 name_tech=request.form['name_tech'],
                                                 comment=request.form['comment'],
                                                 watering_summer=request.form['watering_summer'],
                                                 watering_winter=request.form['watering_winter'],
                                                 spray=request.form['spray'],
                                                 direct_sun=request.form['direct_sun'],
                                                 image=request.form['image'],
                                                 user_id=current_user.id)
            Log.info(f"Plant updated: {plant}")
        else:
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
        Log.error("Error creating/update plant", err=e, sys=sys)
        return render_template('plant_form.html', error=e)

    return render_template('plant_list.html')


@main.route("/plants", methods=['PUT'])
@main.route("/plants/<int:plant_id>", methods=['PUT'])
@login_required
def put_plant(plant_id: int):
    Log.info("Update plant API")
    Log.info(f"Method: {request.method}")
    Log.debug(f"Current user: {current_user}")

    try:
        Log.debug(f"Request form: {request.form}")
        plant_id = plant_id if plant_id else request.form['plant_id']
        plant = ControllerPlant.update_plant(plant_id=plant_id,
                                             name=request.form['name'],
                                             name_tech=request.form['name_tech'],
                                             comment=request.form['comment'],
                                             watering_summer=request.form['watering_summer'],
                                             watering_winter=request.form['watering_winter'],
                                             spray=request.form['spray'],
                                             direct_sun=request.form['direct_sun'],
                                             image=request.form['image'],
                                             user_id=current_user.id)
        Log.info(f"Plant updated: {plant}")
    except Exception as e:
        Log.error("Error updating plant", err=e, sys=sys)
        return render_template('plant_form.html', error=e)

    return render_template('plant_list.html')


# TODO: @main.route("/plants/<int:plant_id>", methods=['DELETE'])
@main.route("/plants/delete/<int:plant_id>")
@login_required
def delete_plant(plant_id: int):
    Log.info("Delete plant API")
    Log.info(f"Method: {request.method}")
    Log.debug(f"Current user: {current_user}")

    ControllerPlant.delete_plant(plant_id)

    all_plants = ControllerPlant.get_all_plants(current_user.id)

    return render_template('plant_list.html', plants=all_plants, message="")


@main.route("/plants/<int:plant_id>/calendar/water", methods=['POST'])
@login_required
def water_plant(plant_id: int):
    Log.info("Water plant page")
    Log.info(f"Method: {request.method}")
    Log.debug(f"Current user: {current_user}")

    pass


@main.route("/plants/<int:plant_id>/calendar/fertilize", methods=['POST'])
@login_required
def fertilize_plant(plant_id: int):
    Log.info("Fertilize plant page")
    Log.info(f"Method: {request.method}")
    Log.debug(f"Current user: {current_user}")

    pass


@main.route("/plants/<int:plant_id>/calendar", methods=['GET'])
@login_required
def view_calendar(plant_id: int):
    Log.info("View calendar page")
    Log.info(f"Method: {request.method}")
    Log.debug(f"Current user: {current_user}")

    pass


@main.route("/plants/<int:plant_id>/calendar/<date>", methods=['GET'])
@login_required
def view_calendar_date(plant_id: int, date_calendar: date):
    Log.info("View calendar date page")
    Log.info(f"Method: {request.method}")
    Log.debug(f"Current user: {current_user}")

    pass


@main.route("/plants/<int:plant_id>/calendar/<date>", methods=['POST'])
@login_required
def add_calendar_date(plant_id: int, date_calendar: date):
    Log.info("Add calendar date page")
    Log.info(f"Method: {request.method}")
    Log.debug(f"Current user: {current_user}")

    pass


@main.route("/plants/<int:plant_id>/calendar/<date>", methods=['PUT'])
@login_required
def update_calendar_date(plant_id: int, date_calendar: date):
    Log.info("Update calendar date page")
    Log.info(f"Method: {request.method}")
    Log.debug(f"Current user: {current_user}")

    pass
