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
from sqlalchemy.orm import validates
from sqlalchemy import inspect
from flask_validator import (ValidateString, ValidateInteger, ValidateEmail, ValidateLessThanOrEqual,
                             ValidateGreaterThanOrEqual, ValidateBoolean)

from .logger import Log
from .config import get_settings

db = SQLAlchemy()


class Plant(db.Model):
    __tablename__ = "t_plant"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    name_tech = db.Column(db.String(100), nullable=True)
    comment = db.Column(db.String(200), nullable=True)
    # Frequency in weeks per month (0-4)
    watering_summer = db.Column(db.Integer, nullable=True, default=1)
    # Frequency in weeks per month (0-4)
    watering_winter = db.Column(db.Integer, nullable=True, default=2)
    spray = db.Column(db.Boolean, nullable=True, default=True)
    # Direct sun value 1: No, 2: Partial, 3: Yes
    direct_sun = db.Column(db.Integer, nullable=True)
    image = db.Column(db.BLOB, nullable=True)
    date_created = db.Column(db.Date, nullable=False, default=date.today)
    date_updated = db.Column(db.Date, nullable=False,
                             default=date.today, onupdate=date.today)
    user_id = db.Column(db.Integer, db.ForeignKey('t_user.id'), nullable=False)

    # TODO: Check to use return "<%r>" % self.name

    def __repr__(self) -> str:
        return f"<Plant {self.name}>"

    # Validations => https://flask-validator.readthedocs.io/en/latest/index.html
    # The __declare_last__() hook allows definition of a class level function that is
    # automatically called by the MapperEvents.after_configured() event, which occurs
    # after mappings are assumed to be completed and the ‘configure’ step has finished.
    @classmethod
    def __declare_last__(cls):
        ValidateString(cls.name, False, True,
                       "Plant name can't be empty or only spaces")
        ValidateInteger(cls.watering_summer, False, True,
                        "Plant watering summer should be a number between 0 and 4")
        ValidateLessThanOrEqual(cls.watering_summer, 4, False, True,
                                "Plant watering summer should be a number between 0 and 4")
        ValidateGreaterThanOrEqual(cls.watering_summer, 0, False, True,
                                   "Plant watering summer should be a number between 0 and 4")
        ValidateInteger(cls.watering_winter, False, True,
                        "Plant watering winter should be a number between 0 and 4")
        ValidateLessThanOrEqual(cls.watering_winter, 4, False, True,
                                "Plant watering winter should be a number between 0 and 4")
        ValidateGreaterThanOrEqual(cls.watering_winter, 0, False, True,
                                   "Plant watering winter should be a number between 0 and 4")
        ValidateBoolean(cls.spray, False, True,
                        "Plant spray should be a boolean")
        ValidateInteger(cls.direct_sun, False, True,
                        "Plant direct sun should be a number between 1 and 3")
        ValidateLessThanOrEqual(cls.direct_sun, 3, False, True,
                                "Plant direct sun should be a number between 1 and 3")
        ValidateGreaterThanOrEqual(
            cls.direct_sun, 1, False, True, "Plant direct sun should be a number between 1 and 3")

    # SQLAlchemy has a built in helped method for using validations, validates(). Its a Server-side validation
    @validates('name')
    def validate_name(self, key, value):
        if not value:
            raise ValueError("Plant name can't be empty")
        return value

    # TODO: Check to use @validates('name_tech', 'comment') => https://stackoverflow.com/a/57294872
    @validates('name_tech', 'comment')
    def validate_empty_string(self, key, value):
        if isinstance(value, str) and value == '':
            return None
        else:
            return value

    # TODO: Check to use serialize()
    # How to serialize SqlAlchemy PostgreSQL query to JSON => https://stackoverflow.com/a/46180522
    def serialize(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}

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
    def create_plant(name: str, name_tech: str, comment: str,
                     watering_summer: int = 1, watering_winter: int = 2,
                     spray: bool = False, direct_sun: int = 1,
                     image=None, user_id: int = None):
        spray = True if spray or spray == "1" else False
        plant = Plant(name=name, name_tech=name_tech, comment=comment, watering_summer=watering_summer,
                      watering_winter=watering_winter, spray=spray, direct_sun=direct_sun,
                      date_created=date.today(), user_id=user_id)
        if plant.name == "" or plant.name is None:
            raise ValueError("Plant name can't be empty")
        if plant.user_id == "" or plant.user_id is None:
            raise ValueError("Plant user_id can't be empty")
        if User.get_user(plant.user_id) is None:
            raise ValueError("Plant user_id doesn't exist")
        db.session.add(plant)
        db.session.commit()
        return plant

    @staticmethod
    def update_plant(plant_id: int, name: str, name_tech: str, comment: str, watering_summer: int,
                     watering_winter: int, spray: bool, direct_sun: int):
        plant = Plant.get_plant(plant_id)
        if plant is None:
            return None
        if User.get_user(plant.user_id) is None:
            raise ValueError("Plant user_id doesn't exist")
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
        if plant is None:
            return None
        db.session.delete(plant)
        db.session.commit()
        return plant


class Calendar(db.Model):
    __tablename__ = "t_calendar"

    date = db.Column(db.Date, primary_key=True)
    water = db.Column(db.Boolean, nullable=False, default=False)
    fertilize = db.Column(db.Boolean, nullable=False, default=False)
    plant_id = db.Column(db.Integer, db.ForeignKey(
        't_plant.id'), nullable=False)

    def __repr__(self) -> str:
        return f"<Calendar {self.date}>"

    @staticmethod
    def get_calendar(plant_id: int):
        return Calendar.query.filter_by(plant_id=plant_id).all()

    @staticmethod
    def get_calendar_date(date: date, plant_id: int):
        return Calendar.query.filter_by(date=date, plant_id=plant_id).first()

    @staticmethod
    def create_calendar(date: date, water: bool, fertilize: bool, plant_id: int):
        calendar = Calendar(date=date, water=water,
                            fertilize=fertilize, plant_id=plant_id)
        db.session.add(calendar)
        db.session.commit()
        return calendar

    @staticmethod
    def delete_calendar_date(date: date, plant_id: int):
        calendar = Calendar.get_calendar_date(date, plant_id)
        if calendar is None:
            return None
        db.session.delete(calendar)
        db.session.commit()
        return calendar

    @staticmethod
    def delete_calendar_plant(plant_id: int):
        calendar = Calendar.get_calendar(plant_id)
        if len(calendar) == 0:
            return None
        for date in calendar:
            db.session.delete(date)
        db.session.commit()
        return calendar


# Flask-Login can manage user sessions. UserMixin will add Flask-Login attributes
# to the model so that Flask-Login will be able to work with it.
class User(UserMixin, db.Model):
    __tablename__ = "t_user"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    date_created = db.Column(db.Date, nullable=False, default=date.today)
    date_updated = db.Column(db.Date, nullable=False,
                             default=date.today, onupdate=date.today)

    def __repr__(self) -> str:
        return f"<User {self.name}>"

    # Validations => https://flask-validator.readthedocs.io/en/latest/index.html
    # The __declare_last__() hook allows definition of a class level function that is
    # automatically called by the MapperEvents.after_configured() event, which occurs
    # after mappings are assumed to be completed and the ‘configure’ step has finished.
    @classmethod
    def __declare_last__(cls):
        ValidateEmail(cls.email, False, True,
                      "User email can't be empty or only spaces")
        ValidateString(cls.name, False, True,
                       "User name can't be empty or only spaces")
        ValidateString(cls.password, False, True,
                       "User password can't be empty or only spaces")

    @staticmethod
    def get_user(id: int):
        return User.query.filter_by(id=id).first()

    @staticmethod
    def get_user_email(email: str):
        return User.query.filter_by(email=email).first()

    @staticmethod
    def get_user_name(name: str):
        return User.query.filter_by(name=name).first()

    @staticmethod
    def delete_user(id: int) -> None:
        User.query.filter_by(id=id).delete()
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

    except Exception as err:  # pragma: no cover
        logging.error(f"Execution Error in init_db: {err}", exc_info=True)


# FORMAT = '%(asctime)s %(levelname)s %(lineno)d %(filename)s %(funcName)s: %(message)s'
# logging.basicConfig(level=logging.INFO, format=FORMAT)

if __name__ == '__main__':  # pragma: no cover # To doesn't check in tests
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
