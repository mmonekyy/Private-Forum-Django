from django.core.management.base import BaseCommand
from forum_posts_sell.models import sell_post , buyed_item
from forum_users.models import CustomUser 
import json
import os

class Command(BaseCommand):
    help = "Crate MarketPlace posts from JSON file"

    def handle(self, *args, **kwargs):
        path = os.path.dirname(__file__)
        with open(f'{path}/posts.json', 'r') as file:
            data = json.load(file)
        for item in data:
            try:
                author = CustomUser.objects.get(id=item['Author'])
            except CustomUser.DoesNotExist:
                print(f"Author with id {item['Author']} not found, skipping post {item['Title']}")
                break
            post, created = sell_post.objects.get_or_create(
                Title=item['Title'],
                Text=item['Text'],
                Price=item['Price'],
                Post_status=item['Post_status'],
                Author=author,
            )
            post.tags.add(*item['tags'])
            post.save()
            buyed_item.objects.get_or_create(
                foring_key_sell_post=post,
                Text=item['prize']
            )

