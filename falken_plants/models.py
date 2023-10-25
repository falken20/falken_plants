# by Richi Rod AKA @richionline / falken20
# ./falken_plants/models.py

# ######################################################################
# This file is to set all the db models and use the ORM flask_sqlalchemy
# ######################################################################

import os
import logging
from datetime import date
from flask import Flask
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

from .logger import Log
from .config import get_settings

db = SQLAlchemy()


class Plant(db.Model):
    __tablename__ = "t_plant"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    name_tech = db.Column(db.String(100), nullable=True)
    comment = db.Column(db.String(200), nullable=True)
    # Frequency in weeks per month (1-4)
    watering_summer = db.Column(db.Integer, nullable=False)
    # Frequency in weeks per month (1-4)
    watering_winter = db.Column(db.Integer, nullable=False)
    spray = db.Column(db.Boolean, nullable=False)
    # Direct sun value 1: No, 2: Partial, 3: Yes
    direct_sun = db.Column(db.Integer, nullable=False)
    date_registration = db.Column(db.Date, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('t_user.id'), nullable=False)

    def __repr__(self) -> str:
        return f"<Plant {self.name}>"

    @staticmethod
    def get_plants(user_id: int):
        return Plant.query.filter_by(user_id=user_id).all()

    @staticmethod
    def get_plant(plant_id: int):
        return Plant.query.filter_by(id=plant_id).first()

    @staticmethod
    def get_plant_name(plant_name: str):
        return Plant.query.filter_by(name=plant_name).first()

    @staticmethod
    def create_plant(name: str, name_tech: str, comment: str, watering_summer: int, watering_winter: int, spray: bool, direct_sun: int, user_id: int):
        plant = Plant(name=name, name_tech=name_tech, comment=comment, watering_summer=watering_summer,
                      watering_winter=watering_winter, spray=spray, direct_sun=direct_sun, date_registration=date.today(), user_id=user_id)
        if plant.name == "":
            raise Exception("Plant name can't be empty")
        db.session.add(plant)
        db.session.commit()
        return plant

    @staticmethod
    def update_plant(plant_id: int, name: str, name_tech: str, comment: str, watering_summer: int, watering_winter: int, spray: bool, direct_sun: int):
        plant = Plant.get_plant(plant_id)
        plant.name = name
        plant.name_tech = name_tech
        plant.comment = comment
        plant.watering_summer = watering_summer
        plant.watering_winter = watering_winter
        plant.spray = spray
        plant.direct_sun = direct_sun
        db.session.commit()
        return plant

    @staticmethod
    def delete_plant(plant_id: int):
        plant = Plant.get_plant(plant_id)
        db.session.delete(plant)
        db.session.commit()
        return plant


class Calendar(db.Model):
    __tablename__ = "t_watering"

    date = db.Column(db.Date, primary_key=True)
    water = db.Column(db.Boolean, nullable=False)
    fertilize = db.Column(db.Boolean, nullable=False)
    plant_id = db.Column(db.Integer, db.ForeignKey(
        't_plant.id'), nullable=False)

    @staticmethod
    def get_calendar(plant_id: int):
        return Calendar.query.filter_by(plant_id=plant_id).all()


# Flask-Login can manage user sessions. UserMixin will add Flask-Login attributes
# to the model so that Flask-Login will be able to work with it.
class User(UserMixin, db.Model):
    __tablename__ = "t_user"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    date_from = db.Column(db.Date, nullable=False)

    @staticmethod
    def get_user_email(email: str):
        return User.query.filter_by(email=email).first()

    @staticmethod
    def get_user_name(name: str):
        return User.query.filter_by(name=name).first()

    @staticmethod
    def delete_user(id: int) -> None:
        User.query.filter(id).delete()
        db.session.commit()


def init_db(app):
    """
    Main process to create the needed tables for the application
    """
    logging.info("Init DB process starting...")

    try:
        if input("Could you drop the tables if they exist(y/n)? ") in ["Y", "y"]:
            with app.app_context():
                db.drop_all()
            logging.info("Tables dropped")

        if input("Could you create the tables(y/n)? ") in ["Y", "y"]:
            logging.info("Creating tables...")
            with app.app_context():
                db.create_all()

        with app.app_context():
            db.session.commit()

        logging.info("Process finished succesfully")

    except Exception as err:
        logging.error(f"Execution Error in init_db: {err}", exc_info=True)


# FORMAT = '%(asctime)s %(levelname)s %(lineno)d %(filename)s %(funcName)s: %(message)s'
# logging.basicConfig(level=logging.INFO, format=FORMAT)

if __name__ == '__main__':
    logging.info("Preparing app vars...")
    app = Flask(__name__)

    if get_settings().ENV_PRO == "N":
        # basedir is the path to the root of the project
        basedir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        Log.info("Running in development mode with sqlite DB")
        Log.info(
            f"DB path: {os.path.join(basedir, 'database.db')}", style="red bold")
        app.config['DEBUG'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
            os.path.join(basedir, 'database.db')
    else:
        Log.info("Running in production mode with postgres DB")
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL'].replace(
            "://", "ql://", 1)

    db.init_app(app)
    init_db(app)
