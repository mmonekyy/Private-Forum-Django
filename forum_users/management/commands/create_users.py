from django.core.management.base import BaseCommand
from forum_users.models import CustomUser
import json
import os
class Command(BaseCommand):
    help = "Create users"

    def handle(self, *args, **kwargs):
        if not CustomUser.objects.exists():
            path = os.path.dirname(__file__)
            with open(f'{path}/users.json', 'r') as file:
                data = json.load(file)
            for user in data:
                CustomUser.objects.create_user(username=user["username"],user_type=user["user_type"],password=user["password"])
            print("users created")
        else:
            print('users exists')