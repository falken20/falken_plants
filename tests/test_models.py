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
        self.assertFalse(user.date_to)
        self.assertFalse(user.admin)
        self.assertFalse(user.active)
        self.assertFalse(user.confirmed)
        self.assertFalse(user.confirmed_on)
        self.assertFalse(user.reset_password_token)
        self.assertFalse(user.reset_password_expires)
        self.assertFalse(user.plants)
        self.assertFalse(user.plant_types)
        self.assertFalse(user.calendar)

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
