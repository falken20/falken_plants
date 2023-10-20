from basetest import BaseTestCase

class TestModels(BaseTestCase):

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