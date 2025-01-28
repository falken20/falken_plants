import unittest

from . import basetest


class TestMain(basetest.BaseTestCase):

    def test_index(self):
        # self.app.config['TESTING'] = True
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_show_grouped(self):
        with self.app.test_client() as client:
            self.app.get('/login', follow_redirects=True)
            response = self.app.get('/show_grouped/')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'plant_list_group.html', response.data)

    def test_profile(self):
        with self.app.test_client() as client:
            self.app.get('/login', follow_redirects=True)
            response = self.client.get('/profile')
            self.assertEqual(response.status_code, 200)
            # Add more assertions as needed
