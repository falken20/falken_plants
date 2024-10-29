# by Richi Rod AKA @richionline / falken20
# ./falken_plants/urls.py

from flask import request

from .main import main
from .controlles import ControllerPlant


@main.route("/plants", methods=['GET', 'POST'])
def list_create_plants():
    if request.method == 'GET': 
        return ControllerPlant.list_all_plants(user_id)
    elif request.method == 'POST':
        return ControllerPlant.create_plant()
    else:
        return "Method not allowed", 405

@main.route("/plants/<int:plant_id>", methods=['GET', 'PUT', 'DELETE'])
def get_update_delete_plants(plant_id):
    if request.method == 'GET':
        return ControllerPlant.get_plant(plant_id)
    elif request.method == 'PUT':
        return ControllerPlant.update_plant(plant_id)
    elif request.method == 'DELETE':
        return ControllerPlant.delete_plant(plant_id)
    else:
        return "Method not allowed", 405