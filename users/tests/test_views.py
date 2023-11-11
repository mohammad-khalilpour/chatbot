from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from users.forms import RegistrationForm

User = get_user_model()


class RegisterViewTests(TestCase):
    def test_successful_registration(self):
        data = {
            'email': 'testuser@example.com',
            'password1': 'TestPassword123',
            'password2': 'TestPassword123',
        }
        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, 200)

    def test_registration_with_different_passwords(self):
        data = {
            'email': 'testuser@example.com',
            'password1': 'TestPassword123',
            'password2': 'DifferentPassword456',
        }
        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, 200, msg='The two password fields didn’t match.')

    def test_registration_with_same_email(self):
        user = User.objects.create_user(email='testuser@example.com', password='TestPassword123')

        data = {
            'email': 'testuser@example.com',
            'password1': 'NewPassword789',
            'password2': 'NewPassword789',
        }
        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, 200, msg='This email address is already in use.')

    def test_register_view_uses_correct_template(self):
        response = self.client.get(reverse('register'))
        self.assertTemplateUsed(response, 'register.html')
