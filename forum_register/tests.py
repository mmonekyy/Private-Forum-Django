from django.test import TestCase
from django.test import Client
from forum_users.models import CustomUser
from .models import Keys
# Create your tests here.

class create_account_test(TestCase):
    def setUp(self):
        Keys.objects.create(key='testkey')
        self.client = Client()
   
    def test_register_viev_get(self):
        response = self.client.get('/register/')
        self.assertEqual(response.status_code, 200)

    def test_register_create(self):
        response = self.client.post('/register/', {
        'username': 'testuser2',
        'password': 'testpass2',
        'password2': 'testpass2',    
        'key': 'testkey',
        'register': 'Submit'
        })
        user = CustomUser.objects.get(username='testuser2')
        self.assertEqual(user.username, 'testuser2')
        self.assertTrue(user.check_password('testpass2'))

    def test_register_create_invalid_key(self):
        response = self.client.post('/register/', {
        'username': 'testuser3',
        'password': 'testpass3',
        'password2': 'testpass3',
        'key': 'invalidkey',
        'register': 'Submit'
        })
        user = CustomUser.objects.filter(username='testuser3').exists()
        self.assertFalse(user)
    
    def test_register_create_password_mismatch(self):
        response = self.client.post('/register/', {
        'username': 'testuser4',
        'password': 'testpass4',
        'password2': 'testpass5',
        'key': 'testkey',
        'register': 'Submit'
        })
        user = CustomUser.objects.filter(username='testuser4').exists()
        self.assertFalse(user)
        
    def test_existing_username(self):
        CustomUser.objects.create_user(username='existinguser', password='existingpass')
        response = self.client.post('/register/', {
        'username': 'existinguser',
        'password': 'newpass',
        'password2': 'newpass',
        'key': 'testkey',
        'register': 'Submit'
        })
        user = CustomUser.objects.filter(username='existinguser').count()
        self.assertEqual(user, 1)