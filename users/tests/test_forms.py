from django.test import TestCase, Client
from users.forms import RegistrationForm, LoginForm
from django.core.exceptions import ValidationError
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


class LoginFormTest(TestCase):
    def setUp(self):
        self.user_data = {
            'email': 'test@example.com',
            'password': 'testpassword',
        }
        self.user = get_user_model().objects.create_user(**self.user_data)

    def test_valid_login(self):
        form_data = {
            'email': 'test@example.com',
            'password': 'testpassword',
        }
        form = LoginForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_inactive_user_login(self):
        self.user.is_active = False
        self.user.save()

        form_data = {
            'email': 'test@example.com',
            'password': 'testpassword',
        }
        form = LoginForm(data=form_data)

        self.assertFalse(form.is_valid())

    def test_invalid_login(self):
        invalid_form_data = {
            'email': 'nonexistent@example.com',
            'password': 'invalidpassword',
        }
        form = LoginForm(data=invalid_form_data)

        self.assertFalse(form.is_valid())

    def test_missing_fields(self):
        form = LoginForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
        self.assertIn('password', form.errors)

