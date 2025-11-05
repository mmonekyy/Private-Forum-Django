from django.test import TestCase
from forum_users.models import CustomUser

class AdminPanelTests(TestCase):
    def setUp(self):
        self.user_admin = CustomUser.objects.create_user(username='testuser', password='12345', user_type=4)
        self.normal_user = self.user = CustomUser.objects.create_user(username='testuser_normal', password='12345')
    
    def test_admin_views_authenticated_as_mod(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get('/ModPanel/')
        self.assertEqual(response.status_code, 200)
        response_two = self.client.get('/ModPanel/sellpost/')
        self.assertEqual(response_two.status_code, 200)
        response_three = self.client.get('/ModPanel/post/')
        self.assertEqual(response_three.status_code, 200)
    
    def test_admin_views_authenticated(self):
        self.client.login(username='testuser_normal', password='12345')
        response = self.client.get('/ModPanel/')
        self.assertEqual(response.status_code, 302)
        response_two = self.client.get('/ModPanel/sellpost/')
        self.assertEqual(response_two.status_code, 302)
        response_three = self.client.get('/ModPanel/post/')
        self.assertEqual(response_three.status_code, 302)

    def test_admin_views_unauthenticated(self):
        self.client.logout()
        response = self.client.get('/ModPanel/')
        self.assertEqual(response.status_code, 302)
        response_two = self.client.get('/ModPanel/sellpost/')
        self.assertEqual(response_two.status_code, 302)
        response_three = self.client.get('/ModPanel/post/')
        self.assertEqual(response_three.status_code, 302)
    

