from .basetest import BaseTestCase
from falken_plants.models import User, Plant


class TestModels(BaseTestCase):

    #### User model tests ####

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

    def test_create_plant_no_user(self):
        self.assertRaises(ValueError, Plant.create_plant, name='',
                          name_tech='test_plant', comment='test_plant')

    def test_get_plants_no_user(self):
        user = self.create_user()
        plant = Plant.create_plant(name='test_plant', name_tech='test_plant', comment='test_plant',
                                   watering_summer=1, watering_winter=1, spray=True, direct_sun=1, user_id=user.id)
        User.delete_user(user.id)
        plants = Plant.get_plants(user_id=user.id)
        self.assertIsNone(plants[0])

    def test_update_plant_no_user(self):
        user = self.create_user()
        plant = Plant.create_plant(name='test_plant', name_tech='test_plant', comment='test_plant',
                                   watering_summer=1, watering_winter=1, spray=True, direct_sun=1, user_id=user.id)
        User.delete_user(user.id)
        self.assertRaises(ValueError, Plant.update_plant, plant_id=1, name='test_plant_update', name_tech='test_plant_update', comment='test_plant_update',
                          watering_summer=2, watering_winter=2, spray=False, direct_sun=2)

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
        plant_delete = Plant.delete_plant(1)
        self.assertFalse(plant_delete)

    def test_create_plant_no_name(self):
        user = self.create_user()
        self.assertRaises(ValueError, Plant.create_plant, name='',
                          name_tech='test_plant', comment='test_plant',)
