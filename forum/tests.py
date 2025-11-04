from django.test import TestCase , Client
from forum_users.models import CustomUser
# Create your tests here.
class ForumTests(TestCase):
    def setUp(self):
        self.username = 'testuser'
        self.password = 'testpassword'
        self.user = CustomUser.objects.create_user(username=self.username, password=self.password)

    def connect_user(self, username, password):
        client = Client()
        login_successful = client.login(username=username, password=password)
        self.assertTrue(login_successful, "Login failed for user: {}".format(username))
        return client

    def test_access_for_logged_user(self):
        client = self.connect_user(self.username, self.password)
        response = client.get('')
        self.assertEqual(response.status_code, 200)

    def test_access_for_anonymous_user(self):
        client = Client()
        response = client.get('')
        self.assertEqual(response.status_code, 302)
    