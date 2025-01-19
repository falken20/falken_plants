# by Richi Rod AKA @richionline / falken20
from datetime import date

from .basetest import BaseTestCase
from falken_plants.models import db, User, Plant, Calendar
from falken_plants.controllers import ControllerPlant, ControllerCalendar, ControllerUser


class TestControllerUser(BaseTestCase):
    def test_create_user(self):
        user = self.create_user()
        self.assertTrue(user.id)
        self.assertEqual(user.email, self.mock_user['email'])
        self.assertEqual(user.name, self.mock_user['name'])
        self.assertTrue(user.password)
        self.assertTrue(user.date_created)

    def test_delete_user(self):
        user = self.create_user()
        self.assertTrue(user.id)
        ControllerUser.delete_user(user.id)
        self.assertFalse(User.query.filter_by(id=user.id).first())

    def test_get_user(self):
        user = self.create_user()
        user_get = ControllerUser.get_user(user.id)
        self.assertEqual(user_get.email, user.email)

    def test_get_user_email(self):
        user = self.create_user()
        user_get = ControllerUser.get_user_email(user.email)
        self.assertEqual(user_get.email, user.email)

    def test_get_user_name(self):
        user = self.create_user()
        user_get = ControllerUser.get_user_name(user.name)
        self.assertEqual(user_get.name, user.name)

    def test_get_user_no_user(self):
        user = ControllerUser.get_user(1)
        self.assertFalse(user)


class TestControllerPlant(BaseTestCase):
    def test_create_plant(self):
        user = self.create_user()
        plant = ControllerPlant.create_plant(name='test_plant', name_tech='test_plant', comment='test_plant',
                                             watering_summer=1, watering_winter=1, spray=True, direct_sun=1, user_id=user.id)
        self.assertTrue(plant.id)
        self.assertEqual(plant.name, 'test_plant')
        self.assertEqual(plant.name_tech, 'test_plant')
        self.assertEqual(plant.comment, 'test_plant')
        self.assertEqual(plant.watering_summer, 1)
        self.assertEqual(plant.watering_winter, 1)
        self.assertTrue(plant.spray)
        self.assertEqual(plant.direct_sun, 1)
        self.assertTrue(plant.date_created)
        self.assertEqual(plant.user_id, user.id)

    def test_get_plants(self):
        user = self.create_user()
        plant = ControllerPlant.create_plant(name='test_plant', name_tech='test_plant', comment='test_plant',
                                             watering_summer=1, watering_winter=1, spray=True, direct_sun=1, user_id=user.id)
        plants = ControllerPlant.list_all_plants(user.id)
        self.assertEqual(len(plants), 1)
        self.assertEqual(plants[0].name, plant.name)

    def test_get_plant(self):
        user = self.create_user()
        plant = ControllerPlant.create_plant(name='test_plant', name_tech='test_plant', comment='test_plant',
                                             watering_summer=1, watering_winter=1, spray=True, direct_sun=1, user_id=user.id)
        plant_get = ControllerPlant.get_plant(plant.id)
        self.assertEqual(plant_get.name, plant.name)

    def test_get_plant_name(self):
        user = self.create_user()
        plant = ControllerPlant.create_plant(name='test_plant', name_tech='test_plant', comment='test_plant',
                                             watering_summer=1, watering_winter=1, spray=True, direct_sun=1, user_id=user.id)
        plant_get = ControllerPlant.get_plant_name(plant.name)
        self.assertEqual(plant_get.name, plant.name)

    def test_update_plant(self):
        user = self.create_user()
        plant = ControllerPlant.create_plant(name='test_plant', name_tech='test_plant', comment='test_plant',
                                             watering_summer=1, watering_winter=1, spray=True, direct_sun=1, user_id=user.id)
        plant_update = ControllerPlant.update_plant(plant.id, name='test_plant_update', name_tech='test_plant_update',
                                                    comment='test_plant_update', watering_summer=2, watering_winter=2,
                                                    spray=False, direct_sun=2)
        self.assertEqual(plant_update.name, 'test_plant_update')
        self.assertEqual(plant_update.name_tech, 'test_plant_update')
        self.assertEqual(plant_update.comment, 'test_plant_update')
        self.assertEqual(plant_update.watering_summer, 2)
        self.assertEqual(plant_update.watering_winter, 2)
        self.assertFalse(plant_update.spray)
        self.assertEqual(plant_update.direct_sun, 2)

    def test_delete_plant(self):
        user = self.create_user()
        plant = ControllerPlant.create_plant(name='test_plant', name_tech='test_plant', comment='test_plant',
                                             watering_summer=1, watering_winter=1,
                                             spray=True, direct_sun=1, user_id=user.id)
        ControllerPlant.delete_plant(plant.id)
        self.assertFalse(Plant.query.filter_by(id=plant.id).first())

    def test_create_plant_no_name(self):
        user = self.create_user()
        self.assertRaises(ValueError, ControllerPlant.create_plant, name='',
                          name_tech='test_plant', comment='test_plant', user_id=user.id)

    def test_create_plant_no_user(self):
        self.assertRaises(ValueError, ControllerPlant.create_plant, name='test_plant',
                          name_tech='test_plant', comment='test_plant')
        self.assertRaises(ValueError, ControllerPlant.create_plant, name='test_plant',
                          name_tech='test_plant', comment='test_plant', user_id=5)

    def test_get_plants_no_user(self):
        user = self.create_user()
        plants = ControllerPlant.list_all_plants(user_id=user.id)
        self.assertEqual(len(plants), 0)

    def test_update_plant_no_user(self):
        user = self.create_user()
        plant = ControllerPlant.create_plant(name='test_plant', name_tech='test_plant', comment='test_plant',
                                             watering_summer=1, watering_winter=1, spray=True,
                                             direct_sun=1, user_id=user.id)
        ControllerUser.delete_user(user.id)
        self.assertRaises(ValueError, ControllerPlant.update_plant, plant_id=plant.id, name='test_plant_update',
                          name_tech='test_plant_update', comment='test_plant_update', watering_summer=2,
                          watering_winter=2, spray=False, direct_sun=2)

    def test_get_plants_no_plants(self):
        user = self.create_user()
        plants = ControllerPlant.list_all_plants(user.id)
        self.assertFalse(plants)

    def test_get_plant_no_plant(self):
        plant = ControllerPlant.get_plant(1)
        self.assertFalse(plant)

    def test_get_plant_name_no_plant(self):
        plant = ControllerPlant.get_plant_name('test_plant')
        self.assertFalse(plant)

    def test_update_plant_no_plant(self):
        plant_update = ControllerPlant.update_plant(1, name='test_plant_update', name_tech='test_plant_update',
                                                    comment='test_plant_update', watering_summer=2, watering_winter=2,
                                                    spray=False, direct_sun=2)
        self.assertFalse(plant_update)

    def test_delete_plant_no_plant(self):
        plant_delete = ControllerPlant.delete_plant(10)
        self.assertFalse(plant_delete)

    def test_create_plant_no_name(self):
        user = self.create_user()
        self.assertRaises(ValueError, ControllerPlant.create_plant, name='',
                          name_tech='test_plant', comment='test_plant',)


class TestControllerCalendar(BaseTestCase):
    def test_create_calendar(self):
        user = self.create_user()
        plant = ControllerPlant.create_plant(name='test_plant', name_tech='test_plant', comment='test_plant',
                                             watering_summer=1, watering_winter=1, spray=True, direct_sun=1, user_id=user.id)
        calendar = ControllerCalendar.create_calendar(
            plant_id=plant.id, date_calendar=date.today(), water=True, fertilize=False)
        self.assertTrue(calendar)
        self.assertEqual(calendar.plant_id, plant.id)
        self.assertEqual(calendar.date_calendar, date.today())

    def test_get_calendar(self):
        user = self.create_user()
        plant = ControllerPlant.create_plant(name='test_plant', name_tech='test_plant', comment='test_plant',
                                             watering_summer=1, watering_winter=1, spray=True, direct_sun=1, user_id=user.id)
        ControllerCalendar.create_calendar(
            plant_id=plant.id, date_calendar=date.today(), water=True, fertilize=False)
        calendar_get = ControllerCalendar.get_calendar(plant_id=plant.id)
        self.assertIsInstance(calendar_get, list)
        self.assertEqual(calendar_get[0].plant_id, plant.id)

    def test_get_calendar_date(self):
        user = self.create_user()
        plant = ControllerPlant.create_plant(name='test_plant', name_tech='test_plant', comment='test_plant',
                                             watering_summer=1, watering_winter=1,
                                             spray=True, direct_sun=1, user_id=user.id)
        ControllerCalendar.create_calendar(
            plant_id=plant.id, date_calendar=date.today(), water=True, fertilize=False)
        calendar_get = ControllerCalendar.get_calendar_date(
            plant_id=plant.id, date_calendar=date.today())
        self.assertIsInstance(calendar_get, Calendar)
        self.assertEqual(calendar_get.plant_id, plant.id)
        self.assertEqual(calendar_get.date_calendar, date.today())

    def test_delete_calendar_date(self):
        user = self.create_user()
        plant = ControllerPlant.create_plant(name='test_plant', name_tech='test_plant',
                                             comment='test_plant', watering_summer=1, watering_winter=1,
                                             spray=True, direct_sun=1, user_id=user.id)
        ControllerCalendar.create_calendar(
            plant_id=plant.id, date_calendar=date.today(), water=True, fertilize=False)
        ControllerCalendar.delete_calendar_date(
            plant_id=plant.id, date_calendar=date.today())
        calendar_get = ControllerCalendar.get_calendar_date(
            date_calendar=date.today(), plant_id=plant.id)
        self.assertFalse(calendar_get)
        # Test delete calendar None
        calendar_delete = ControllerCalendar.delete_calendar_date(
            plant_id=plant.id, date_calendar=date.today())
        self.assertFalse(calendar_delete)

    def test_delete_calendar_plant(self):
        user = self.create_user()
        plant = ControllerPlant.create_plant(name='test_plant', name_tech='test_plant',
                                             comment='test_plant', watering_summer=1, watering_winter=1,
                                             spray=True, direct_sun=1, user_id=user.id)
        ControllerCalendar.create_calendar(
            plant_id=plant.id, date_calendar=date.today(), water=True, fertilize=False)
        ControllerCalendar.delete_calendar_plant(plant_id=plant.id)
        calendar_get = ControllerCalendar.get_calendar(plant_id=plant.id)
        self.assertFalse(calendar_get)
        # Test delete calendar plant None
        calendar_delete = ControllerCalendar.delete_calendar_plant(
            plant_id=plant.id)
        self.assertFalse(calendar_delete)
