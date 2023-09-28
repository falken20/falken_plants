# by Richi Rod AKA @richionline / falken20
# ./falken_plants/main.py

from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from datetime import datetime
from functools import lru_cache

from .logger import Log
from .models import Teleworking, User
from .config import get_settings

main = Blueprint('main', __name__)

previous_cache = datetime.now()


@main.route("/", methods=('GET', 'POST'))
@main.route("/home", methods=('GET', 'POST'))
@login_required
def index():
    pass      