from django.test import TestCase
from .models import CustomUser
# Create your tests here.

class custom_user_test_case(TestCase):
    def setUp(self):
        CustomUser.objects.create_user(username='testuser1', password='testpass1')

    def test_user_creation(self):
        user = CustomUser.objects.get(username='testuser1')
        self.assertEqual(user.username, 'testuser1')
        self.assertTrue(user.check_password('testpass1'))