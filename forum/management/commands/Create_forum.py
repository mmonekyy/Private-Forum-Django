from django.core.management.base import BaseCommand
from forum_users.models import CustomUser
import json
import os
class Command(BaseCommand):
    help = "Create users"

    def handle(self, *args, **kwargs):
        print("Creating users...")
        