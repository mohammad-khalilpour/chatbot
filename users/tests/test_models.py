from django.test import TestCase
from django.contrib.auth import get_user_model


class UserModelTests(TestCase):
    def setUp(self):
        self.user_data = {
            'email': 'test@example.com',
            'password': 'testpassword',
            'is_chatbot_creator': True,
        }

    def test_create_user(self):
        user = get_user_model()
        user = user.objects.create_user(**self.user_data)

        self.assertEqual(user.email, self.user_data['email'])
        self.assertTrue(user.check_password(self.user_data['password']))
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertTrue(user.is_chatbot_creator)

    def test_create_superuser(self):
        user = get_user_model()
        admin_user = user.objects.create_superuser(**self.user_data)

        self.assertEqual(admin_user.email, self.user_data['email'])
        self.assertTrue(admin_user.check_password(self.user_data['password']))
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        self.assertTrue(admin_user.is_chatbot_creator)

