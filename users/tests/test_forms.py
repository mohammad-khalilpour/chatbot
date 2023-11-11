from django.test import TestCase, Client
from users.forms import RegistrationForm
from django.contrib.auth import get_user_model

User = get_user_model()


class RegistrationFormTestCase(TestCase):
    def setUp(self):
        User.objects.create(email="test@gmail.com", password="password123")

    def test_valid_form(self):
        test_data = {
            'email': 'testuser@example.com',
            'password1': 'TestPassword123',
            'password2': 'TestPassword123',
        }
        form = RegistrationForm(data=test_data)

        self.assertTrue(form.is_valid())

    def test_invalid_email(self):
        test_data = {'email': 'test@gmail.com',
                     'password1': 'password',
                     'password2': 'password'}

        form = RegistrationForm(data=test_data)

        self.assertFalse(form.is_valid())

        self.assertIn('This email address is already in use.', form.errors['email'])
