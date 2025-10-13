from django.core.management.base import BaseCommand
from forum_post.models import ForumPost , Category
import json
import os

class Command(BaseCommand):
    help = "Create Posts"

    def handle(self, *args, **kwargs):
        path = os.path.dirname(__file__)
        with open(f'{path}/category.json', 'r') as file:
            data = json.load(file)
        if Category.objects.exists():
            print('categories exists')
        else:
            for category in data:
                Category.objects.get_or_create(Name=category["Name"],Description=category["Description"])
            print("categories created")
        with open(f'{path}/posts.json', 'r') as file:
            data = json.load(file)
        if ForumPost.objects.exists():
            print('posts exists')
        else:
            for post in data:
                category_instance = Category.objects.get(id=post["category"])

                c_post, created = ForumPost.objects.get_or_create(
                    Title=post["title"],
                    Category=category_instance,
                    Content=post["content"],
                    Author_id=post["author"],
                )

                c_post.tags.add(*post["tags"])
                c_post.save()


            print("posts created")