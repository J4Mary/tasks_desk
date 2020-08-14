from django.test import TestCase, Client

# Create your tests here.
from users import models


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
            password1=self.default_password,
            password2=self.default_password
            )
        response = self.client.post('/users/register/', user_data)
        pass
        #self.assertEqual(response.status_code, 302)
        #self.assertEqual(response.url, '/')
        #self.assertEqual(models.User.objects.count(), 1)
        #self.assertEqual(models.User.objects.first().username, self.default_username)