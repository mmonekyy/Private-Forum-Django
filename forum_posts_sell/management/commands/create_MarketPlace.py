from django.core.management.base import BaseCommand
from forum_posts_sell.models import sell_post, buyed_item, opinion
from forum_users.models import CustomUser
import json
import os
import random

class Command(BaseCommand):
    help = "Create Marketplace posts from JSON file and add opinions"

    def handle(self, *args, **kwargs):
        path = os.path.dirname(__file__)
        with open(f"{path}/posts.json", "r", encoding="utf-8") as file:
            data = json.load(file)

        users = list(CustomUser.objects.all())

        for item in data:
            author = CustomUser.objects.get(id=item['Author'])
            post = sell_post.objects.create(
                Title=item['Title'],
                Text=item['Text'],
                Price=item['Price'],
                Post_status=item['Post_status'],
                Author=author,
            )
            post.tags.add(*item['tags'])
            post.save()

            buyed_item.objects.create(
                foring_key_sell_post=post,
                Text=item['prize']
            )

            for _ in range(random.randint(2, 6)):
                reviewer = random.choice(users)
                rating = random.randint(1, 5)
                opinion.objects.create(
                    foring_key_buy_item=post,
                    Author=reviewer,
                    Rate=rating
                )
