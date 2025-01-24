import unittest
from flask import Flask
from flask_login import LoginManager, UserMixin

from .basetest import BaseTestCase
from falken_plants import main as main_blueprint

class User(UserMixin):
    def __init__(self, id):
        self.id = id


class MainTestCase(BaseTestCase):

    def test_index(self):
        self.app.register_blueprint(main_blueprint)
        self.app.config['TESTING'] = True
        with self.app.test_client() as client:
            response = client.get('/')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'plant_list.html', response.data)

    def test_show_grouped(self):
        with self.app:
            self.app.get('/login', follow_redirects=True)
            response = self.app.get('/show_grouped/')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'plant_list_group.html', response.data)

    def test_profile(self):
        with self.app:
            self.app.get('/login', follow_redirects=True)
            response = self.client.get('/profile')
            self.assertEqual(response.status_code, 200)
            # Add more assertions as needed


if __name__ == '__main__':
    unittest.main()
