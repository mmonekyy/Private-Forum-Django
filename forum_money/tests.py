from django.test import TestCase
from forum_users.models import CustomUser

class MoneyViewTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')

    def test_points_view_authenticated(self):
        response = self.client.get('/Money/')
        self.assertEqual(response.status_code, 200)
        response_two = self.client.post('/Money/ranks/')
        self.assertEqual(response_two.status_code, 200)
        response_three = self.client.post('/Money/leaderboard/')
        self.assertEqual(response_three.status_code, 200)
    
    def test_points_view_unauthenticated(self):
        self.client.logout()
        response = self.client.get('/Money/')
        self.assertEqual(response.status_code, 400)
        response_two = self.client.post('/Money/ranks/')
        self.assertEqual(response_two.status_code, 400)
        response_three = self.client.post('/Money/leaderboard/')
        self.assertEqual(response_three.status_code, 400)
    
    