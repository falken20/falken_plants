# by Richi Rod AKA @richionline / falken20
from datetime import date

from .models import db, Plant, Calendar, User
from .logger import Log
from .config import shorten_url

# The CRUD operations use to return a JSON response:
# return jsonify(response)


class ControllerPlant:
    def __init__(self):
        pass

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
                     image=None, user_id: int = None) -> Plant:
        Log.info(f"Creating plant: {name}")
        Log.debug(f"Params method: {locals()}")
        # TODO: Check if the image is a valid URL
        # image = shorten_url(image) if image is not None else None
        Log.debug(f"Image shortened: {image}")
        spray = True if spray or spray == "1" else False
        plant = Plant(name=name, name_tech=name_tech, comment=comment, watering_summer=int(watering_summer),
                      watering_winter=int(watering_winter), spray=spray, direct_sun=int(direct_sun),
                      image=image, date_created=date.today(), user_id=user_id)
        if plant.name == "" or plant.name is None:
            raise ValueError("Plant name can't be empty")
        if plant.user_id == "" or plant.user_id is None:
            raise ValueError("Plant user_id can't be empty")
        if ControllerUser.get_user(plant.user_id) is None:
            raise ValueError("Plant user_id doesn't exist")
        db.session.add(plant)
        db.session.commit()
        return plant

    @staticmethod
    def update_plant(plant_id: int, name: str, name_tech: str, comment: str, watering_summer: int,
                     watering_winter: int, spray: bool, direct_sun: int, image: str) -> Plant:
        Log.debug(f"Params method: {locals()}")
        plant = ControllerPlant.get_plant(plant_id)
        if plant is None:
            return None
        if ControllerUser.get_user(plant.user_id) is None:
            raise ValueError("Plant user_id doesn't exist")
        plant.name = name
        plant.name_tech = name_tech
        plant.comment = comment
        plant.watering_summer = watering_summer
        plant.watering_winter = watering_winter
        plant.spray = True if spray or spray == "1" else False
        plant.direct_sun = direct_sun
        plant.image = shorten_url(image) if image is not None else None
        db.session.commit()
        return plant

    @staticmethod
    def delete_plant(plant_id: int):
        plant = ControllerPlant.get_plant(plant_id)
        if plant is None:
            return None
        db.session.delete(plant)
        db.session.commit()
        return plant

    @staticmethod
    def get_all_plants(user_id: int):
        return Plant.query.filter(Plant.user_id == user_id).order_by(Plant.name).all()


class ControllerCalendar:
    def __init__(self):
        pass

    @staticmethod
    def get_calendar(plant_id: int):
        return Calendar.query.filter_by(plant_id=plant_id).all()

    @staticmethod
    def get_calendar_date(date_calendar: date, plant_id: int):
        return Calendar.query.filter_by(date_calendar=date_calendar, plant_id=plant_id).first()

    @staticmethod
    def create_calendar(date_calendar: date, water: bool, fertilize: bool, plant_id: int):
        calendar = Calendar(date_calendar=date_calendar, water=water,
                            fertilize=fertilize, plant_id=plant_id)
        Log.debug(f"Params method: {locals()}")
        db.session.add(calendar)
        db.session.commit()
        return calendar

    @staticmethod
    def delete_calendar_date(date_calendar: date, plant_id: int):
        calendar = ControllerCalendar.get_calendar_date(date_calendar, plant_id)
        if calendar is None:
            return None
        db.session.delete(calendar)
        db.session.commit()
        return calendar

    @staticmethod
    def delete_calendar_plant(plant_id: int):
        calendar = ControllerCalendar.get_calendar(plant_id)
        if len(calendar) == 0:
            return None
        for date_calendar in calendar:
            db.session.delete(date_calendar)
        db.session.commit()
        return calendar


class ControllerUser:
    def __init__(self):
        pass

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
