from django.test import TestCase, Client

# Create your tests here.
from users import models
from cards import models as card_models


class SignupTestCase(TestCase):
    def setUp(self):
        self.default_username = 'test_user'
        self.default_password = '1234567890'
        self.default_email = 'user@gmail.com'
        super(SignupTestCase, self).__init__()
        self.client = Client()

    def test_user_able_to_register(self):
        user_data = dict(
            username=self.default_username,
            email=self.default_email,
            password=self.default_password,
            password2=self.default_password
            )
        response = self.client.post('/users/register/', user_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')
        self.assertEqual(models.User.objects.count(), 1)
        self.assertEqual(models.User.objects.first().username, self.default_username)

    def test_user_unable_to_register(self):
        user_data = dict(
            username=self.default_username,
            email=self.default_email,
            password=self.default_password,
            password2=self.default_password + '1'
        )
        response = self.client.post('/users/register/', user_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(models.User.objects.count(), 0)

    def test_user_able_to_logout(self):
        user_data = dict(
            username=self.default_username,
            email=self.default_email,
            password=self.default_password,
            password2=self.default_password
        )
        self.client.post('/users/register/', user_data)
        response = self.client.post('/users/logout/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')

    def test_user_able_to_login(self):
        user_data = dict(
            username=self.default_username,
            email=self.default_email,
            password=self.default_password,
            password2=self.default_password
        )
        self.client.post('/users/register/', user_data)
        self.client.post('/users/logout/')
        login_data = dict(
            username=self.default_username,
            password=self.default_password
        )
        response = self.client.post('/users/login/', login_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')

    def test_user_unable_to_login(self):
        user_data = dict(
            username=self.default_username,
            email=self.default_email,
            password=self.default_password,
            password2=self.default_password
        )
        self.client.post('/users/register/', user_data)
        self.client.post('/users/logout/')
        login_data = dict(
            username=self.default_username,
            password=self.default_password + '1'
        )
        response = self.client.post('/users/login/', login_data)
        self.assertEqual(response.status_code, 200)
