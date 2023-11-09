# by Richi Rod AKA @richionline / falken20

from datetime import date
from io import StringIO
from unittest.mock import patch

from .basetest import BaseTestCase
from falken_plants.models import User, Plant, Calendar, init_db, db


class TestModelUser(BaseTestCase):
    #### User model tests ####
    def test_repr(self):
        self.assertIn('<User', str(User()))

    def test_create_user(self):
        user = self.create_user()
        self.assertTrue(user.id)
        self.assertEqual(user.email, self.mock_user['email'])
        self.assertEqual(user.name, self.mock_user['name'])
        self.assertTrue(user.password)
        self.assertTrue(user.date_from)

    def test_delete_user(self):
        user = self.create_user()
        self.assertTrue(user.id)
        User.delete_user(user.id)
        self.assertFalse(User.query.filter_by(id=user.id).first())

    def test_get_user(self):
        user = self.create_user()
        user_get = User.get_user(user.id)
        self.assertEqual(user_get.email, user.email)

    def test_get_user_email(self):
        user = self.create_user()
        user_get = User.get_user_email(user.email)
        self.assertEqual(user_get.email, user.email)

    def test_get_user_name(self):
        user = self.create_user()
        user_get = User.get_user_name(user.name)
        self.assertEqual(user_get.name, user.name)

    def test_get_user_no_user(self):
        user = User.get_user(1)
        self.assertFalse(user)


class TestModelPlant(BaseTestCase):
    #### Plant model tests ####
    def test_repr(self):
        self.assertIn('<Plant', str(Plant()))

    def test_create_plant(self):
        user = self.create_user()
        plant = Plant.create_plant(name='test_plant', name_tech='test_plant', comment='test_plant',
                                   watering_summer=1, watering_winter=1, spray=True, direct_sun=1, user_id=user.id)
        self.assertTrue(plant.id)
        self.assertEqual(plant.name, 'test_plant')
        self.assertEqual(plant.name_tech, 'test_plant')
        self.assertEqual(plant.comment, 'test_plant')
        self.assertEqual(plant.watering_summer, 1)
        self.assertEqual(plant.watering_winter, 1)
        self.assertTrue(plant.spray)
        self.assertEqual(plant.direct_sun, 1)
        self.assertTrue(plant.date_registration)
        self.assertEqual(plant.user_id, user.id)

    def test_get_plants(self):
        user = self.create_user()
        plant = Plant.create_plant(name='test_plant', name_tech='test_plant', comment='test_plant',
                                   watering_summer=1, watering_winter=1, spray=True, direct_sun=1, user_id=user.id)
        plants = Plant.get_plants(user.id)
        self.assertEqual(len(plants), 1)
        self.assertEqual(plants[0].name, plant.name)

    def test_get_plant(self):
        user = self.create_user()
        plant = Plant.create_plant(name='test_plant', name_tech='test_plant', comment='test_plant',
                                   watering_summer=1, watering_winter=1, spray=True, direct_sun=1, user_id=user.id)
        plant_get = Plant.get_plant(plant.id)
        self.assertEqual(plant_get.name, plant.name)

    def test_get_plant_name(self):
        user = self.create_user()
        plant = Plant.create_plant(name='test_plant', name_tech='test_plant', comment='test_plant',
                                   watering_summer=1, watering_winter=1, spray=True, direct_sun=1, user_id=user.id)
        plant_get = Plant.get_plant_name(plant.name)
        self.assertEqual(plant_get.name, plant.name)

    def test_update_plant(self):
        user = self.create_user()
        plant = Plant.create_plant(name='test_plant', name_tech='test_plant', comment='test_plant',
                                   watering_summer=1, watering_winter=1, spray=True, direct_sun=1, user_id=user.id)
        plant_update = Plant.update_plant(plant.id, name='test_plant_update', name_tech='test_plant_update', comment='test_plant_update',
                                          watering_summer=2, watering_winter=2, spray=False, direct_sun=2)
        self.assertEqual(plant_update.name, 'test_plant_update')
        self.assertEqual(plant_update.name_tech, 'test_plant_update')
        self.assertEqual(plant_update.comment, 'test_plant_update')
        self.assertEqual(plant_update.watering_summer, 2)
        self.assertEqual(plant_update.watering_winter, 2)
        self.assertFalse(plant_update.spray)
        self.assertEqual(plant_update.direct_sun, 2)

    def test_delete_plant(self):
        user = self.create_user()
        plant = Plant.create_plant(name='test_plant', name_tech='test_plant', comment='test_plant',
                                   watering_summer=1, watering_winter=1, spray=True, direct_sun=1, user_id=user.id)
        Plant.delete_plant(plant.id)
        self.assertFalse(Plant.query.filter_by(id=plant.id).first())

    def test_create_plant_no_name(self):
        user = self.create_user()
        self.assertRaises(ValueError, Plant.create_plant, name='',
                          name_tech='test_plant', comment='test_plant', user_id=user.id)

    def test_create_plant_no_user(self):
        self.assertRaises(ValueError, Plant.create_plant, name='test_plant',
                          name_tech='test_plant', comment='test_plant')
        self.assertRaises(ValueError, Plant.create_plant, name='test_plant',
                          name_tech='test_plant', comment='test_plant', user_id=5)

    def test_get_plants_no_user(self):
        user = self.create_user()
        plants = Plant.get_plants(user_id=user.id)
        self.assertEqual(len(plants), 0)

    def test_update_plant_no_user(self):
        user = self.create_user()
        plant = Plant.create_plant(name='test_plant', name_tech='test_plant', comment='test_plant',
                                   watering_summer=1, watering_winter=1, spray=True, direct_sun=1, user_id=user.id)
        User.delete_user(user.id)
        self.assertRaises(ValueError, Plant.update_plant, plant_id=plant.id, name='test_plant_update', name_tech='test_plant_update',
                          comment='test_plant_update', watering_summer=2, watering_winter=2, spray=False, direct_sun=2)

    def test_get_plants_no_plants(self):
        user = self.create_user()
        plants = Plant.get_plants(user.id)
        self.assertFalse(plants)

    def test_get_plant_no_plant(self):
        plant = Plant.get_plant(1)
        self.assertFalse(plant)

    def test_get_plant_name_no_plant(self):
        plant = Plant.get_plant_name('test_plant')
        self.assertFalse(plant)

    def test_update_plant_no_plant(self):
        plant_update = Plant.update_plant(1, name='test_plant_update', name_tech='test_plant_update', comment='test_plant_update',
                                          watering_summer=2, watering_winter=2, spray=False, direct_sun=2)
        self.assertFalse(plant_update)

    def test_delete_plant_no_plant(self):
        plant_delete = Plant.delete_plant(10)
        self.assertFalse(plant_delete)

    def test_create_plant_no_name(self):
        user = self.create_user()
        self.assertRaises(ValueError, Plant.create_plant, name='',
                          name_tech='test_plant', comment='test_plant',)


class TestModelCalendar(BaseTestCase):
    #### Calendar model tests ####
    def test_repr(self):
        self.assertIn('<Calendar', str(Calendar()))

    def test_create_calendar(self):
        user = self.create_user()
        plant = Plant.create_plant(name='test_plant', name_tech='test_plant', comment='test_plant',
                                   watering_summer=1, watering_winter=1, spray=True, direct_sun=1, user_id=user.id)
        calendar = Calendar(plant_id=plant.id, date=date.today())
        self.assertTrue(calendar)
        self.assertEqual(calendar.plant_id, plant.id)
        self.assertEqual(calendar.date, date.today())

    def test_get_calendar(self):
        user = self.create_user()
        plant = Plant.create_plant(name='test_plant', name_tech='test_plant', comment='test_plant',
                                   watering_summer=1, watering_winter=1, spray=True, direct_sun=1, user_id=user.id)
        Calendar.create_calendar(
            plant_id=plant.id, date=date.today(), water=True, fertilize=False)
        calendar_get = Calendar.get_calendar(plant_id=plant.id)
        self.assertIsInstance(calendar_get, list)
        self.assertEqual(calendar_get[0].plant_id, plant.id)

    def test_get_calendar_date(self):
        user = self.create_user()
        plant = Plant.create_plant(name='test_plant', name_tech='test_plant', comment='test_plant',
                                   watering_summer=1, watering_winter=1, spray=True, direct_sun=1, user_id=user.id)
        Calendar.create_calendar(
            plant_id=plant.id, date=date.today(), water=True, fertilize=False)
        calendar_get = Calendar.get_calendar_date(
            plant_id=plant.id, date=date.today())
        self.assertIsInstance(calendar_get, Calendar)
        self.assertEqual(calendar_get.plant_id, plant.id)
        self.assertEqual(calendar_get.date, date.today())

    def test_delete_calendar_date(self):
        user = self.create_user()
        plant = Plant.create_plant(name='test_plant', name_tech='test_plant',
                                   comment='test_plant', watering_summer=1, watering_winter=1, spray=True, direct_sun=1, user_id=user.id)
        Calendar.create_calendar(
            plant_id=plant.id, date=date.today(), water=True, fertilize=False)
        Calendar.delete_calendar_date(
            plant_id=plant.id, date=date.today())
        calendar_get = Calendar.get_calendar_date(
            plant_id=plant.id, date=date.today())
        self.assertFalse(calendar_get)
        # Test delete calendar None
        calendar_delete = Calendar.delete_calendar_date(
            plant_id=plant.id, date=date.today())
        self.assertFalse(calendar_delete)

    def test_delete_calendar_plant(self):
        user = self.create_user()
        plant = Plant.create_plant(name='test_plant', name_tech='test_plant',
                                   comment='test_plant', watering_summer=1, watering_winter=1, spray=True, direct_sun=1, user_id=user.id)
        Calendar.create_calendar(
            plant_id=plant.id, date=date.today(), water=True, fertilize=False)
        Calendar.delete_calendar_plant(plant_id=plant.id)
        calendar_get = Calendar.get_calendar(plant_id=plant.id)
        self.assertFalse(calendar_get)
        # Test delete calendar plant None
        calendar_delete = Calendar.delete_calendar_plant(plant_id=plant.id)
        self.assertFalse(calendar_delete)


class TestInitDB(BaseTestCase):
    #### init_db tests ####
    def test_init_db_vars(self):
        self.assertTrue(db)
        self.assertTrue(self.app)

    @patch('sys.stdin', StringIO('N\nN\n'))  # Simulate user input
    def test_init_db(self):
        init_db(self.app)

    @patch('sys.stdin', StringIO('Y\nY\n'))  # Simulate user input
    def test_init_db_with_drops(self):
        init_db(self.app)

    @patch('sys.stdin', StringIO('N\nY\n'))  # Simulate user input
    def test_init_db_with_create(self):
        init_db(self.app)
