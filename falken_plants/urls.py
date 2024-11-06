# by Richi Rod AKA @richionline / falken20
# ./falken_plants/urls.py
from flask import request, redirect, url_for, Blueprint, render_template
from flask_login import login_required, current_user
from datetime import date

from .controllers import ControllerPlant

urls = Blueprint('urls', __name__)

# API Plants


@urls.route("/plants", methods=['GET', 'POST'])
@login_required
def list_create_plants():
    Log.info("GET or POST plants API")
    Log.info(f"Method: {request.method}")
    Log.debug(f"Current user: {current_user}")
    if request.method == 'GET':
        all_plants = ControllerPlant.list_all_plants(user_id)
        return render_template('plant_list.html', plants=all_plants, message="")
    elif request.method == 'POST':
        return post_plant()
    else:
        return "Method not allowed", 405


@urls.route("/plants/<int:plant_id>", methods=['GET', 'PUT', 'DELETE'])
@login_required
def get_update_delete_plants(plant_id):
    Log.info("GET, PUT or DELETE plants API")
    Log.info(f"Method: {request.method}")
    Log.debug(f"Current user: {current_user}")
    if request.method == 'GET':
        # TODO: Make it work and make form read_only
        plant = ControllerPlant.get_plant(plant_id)
        return render_template('plant_form.html', plant=plant, form_method="GET")
    elif request.method == 'PUT':
        return put_plant(plant_id)
    elif request.method == 'DELETE':
        ControllerPlant.delete_plant(plant_id)
        all_plants = ControllerPlant.list_all_plants(current_user.id)
        return render_template('plant_list.html', plants=all_plants, message="")
    else:
        return "Method not allowed", 405


# API Pages Plants

@urls.route("/plants/create", methods=['GET'])
@login_required
def page_create_plant():
    Log.info("Create plant page")
    Log.info(f"Method: {request.method}")
    Log.debug(f"Current user: {current_user}")

    return render_template('plant_form.html', plant=None, form_method="POST")


@urls.route("/plants/update/<int:plant_id>", methods=['GET'])
@login_required
def page_update_plant(plant_id: int):
    Log.info("Edit plant page")
    Log.info(f"Method: {request.method}")
    Log.debug(f"Current user: {current_user}")

    plant = ControllerPlant.get_plant(plant_id)
    Log.debug(f"Plant to update: {plant}")

    return render_template('plant_form.html', plant=plant, form_method="PUT")


# Auxiliary methods API Plants

@login_required
def post_plant():
    # Because HTML doesn't support PUT method, we use a hidden field to know if its a PUT method
    Log.info("Method post_plant")
    Log.info(f"Hidden Method: {request.form['_method']}")

    try:
        Log.debug(f"Request form: {request.form}")
        # Because HTML doesn't support PUT method, we use a hidden field to know if its a PUT method
        if request.form['_method'] == "PUT":
            Log.info("Hidden PUT method: Update the plant")
            # Log.info(f"Its a PUT method, redirect to update plant API: /plants/{request.form['id']}")
            # return redirect(f"/plants/{request.form['id']}")
            # return redirect(url_for('main.put_plant', plant_id=request.form['id'], method='PUT'))
            # put_plant(request.form['id'])

            plant = ControllerPlant.update_plant(plant_id=request.form['id'],
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
        else:  # Its a POST method
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
        return render_template('plant_form.html', plant=plant, form_method=request.form['_method'], error=e)

    return redirect(f"/plants/")


@login_required
def put_plant(plant_id: int):
    Log.info("Method put_plant")
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


# TODO: Review rest of API Plants methods
# Other API Plants

@urls.route("/plants/<int:plant_id>/calendar/water", methods=['POST'])
@login_required
def water_plant(plant_id: int):
    Log.info("Water plant page")
    Log.info(f"Method: {request.method}")
    Log.debug(f"Current user: {current_user}")

    pass


@urls.route("/plants/<int:plant_id>/calendar/fertilize", methods=['POST'])
@login_required
def fertilize_plant(plant_id: int):
    Log.info("Fertilize plant page")
    Log.info(f"Method: {request.method}")
    Log.debug(f"Current user: {current_user}")

    pass


@urls.route("/plants/<int:plant_id>/calendar", methods=['GET'])
@login_required
def view_calendar(plant_id: int):
    Log.info("View calendar page")
    Log.info(f"Method: {request.method}")
    Log.debug(f"Current user: {current_user}")

    pass


@urls.route("/plants/<int:plant_id>/calendar/<date>", methods=['GET'])
@login_required
def view_calendar_date(plant_id: int, date_calendar: date):
    Log.info("View calendar date page")
    Log.info(f"Method: {request.method}")
    Log.debug(f"Current user: {current_user}")

    pass


@urls.route("/plants/<int:plant_id>/calendar/<date>", methods=['POST'])
@login_required
def add_calendar_date(plant_id: int, date_calendar: date):
    Log.info("Add calendar date page")
    Log.info(f"Method: {request.method}")
    Log.debug(f"Current user: {current_user}")

    pass


@urls.route("/plants/<int:plant_id>/calendar/<date>", methods=['PUT'])
@login_required
def update_calendar_date(plant_id: int, date_calendar: date):
    Log.info("Update calendar date page")
    Log.info(f"Method: {request.method}")
    Log.debug(f"Current user: {current_user}")

    pass
