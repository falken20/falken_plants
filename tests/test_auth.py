# by Richi Rod AKA @richionline / falken20

import unittest

from . import basetest

class TestAuth(basetest.BaseTestCase):
    def test_auth_login(self):
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)

    def test_auth_login_post(self):
        response = self.client.post('/login', data=self.mock_user, follow_redirects=True)
        self.assertEqual(response.status_code, 200)