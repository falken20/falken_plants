import unittest

from . import basetest


class TestUrls(basetest.BaseTestCase):

    def test_list_create_plants(self):
        # First we need to create a user and login
        self.create_user()
        self.login_http(self)

        response = self.client.get('/plants')
        self.assertEqual(response.status_code, 200)
        # self.assertIn(b'plant_list.html', response.data)

    def test_list_create_plants_post(self):
        self.create_user()
        self.login_http(self)
        response = self.client.post('/plants', data={'name': 'Test Plant', '_method': 'POST'})
        # Assuming redirect after post
        self.assertEqual(response.status_code, 302)

    def test_get_update_delete_plants_get(self):
        self.create_user()
        self.login_http(self)
        response = self.client.get('/plants/1')
        self.assertEqual(response.status_code, 200)
        # self.assertIn(b'plant_form.html', response.data)

    def test_view_create_plant(self):
        self.create_user()
        self.login_http(self)
        response = self.client.get('/plants/create')
        self.assertEqual(response.status_code, 200)
        # self.assertIn(b'plant_form.html', response.data)

    def test_view_update_plant(self):
        self.create_user()
        self.login_http(self)
        response = self.client.get('/plants/update/1')
        self.assertEqual(response.status_code, 200)
        # self.assertIn(b'plant_form.html', response.data)


if __name__ == '__main__':
    unittest.main()
