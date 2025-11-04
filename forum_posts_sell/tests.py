from django.test import TestCase
from forum_users.models import CustomUser
# Create your tests here.
class ForumPostsSellTests(TestCase):
    def setUp(self):
        CustomUser.objects.create_user(username='testuser1', password='testpass1')
    