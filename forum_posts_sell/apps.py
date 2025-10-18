from django.apps import AppConfig
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler import schedulers
import os

def check_posts_date():
    from .models import sell_post
    from django.utils import timezone
    print('Checking posts date...')
    curent_time = timezone.now()
    sell_post.objects.filter(Post_life__lt=curent_time).delete()
    

class ForumPostsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'forum_posts_sell'
    
    def ready(self):
        if os.environ.get('RUN_MAIN') == 'true':
            print('## Starting scheduler for checking posts date... ##')
            self.schedulers = BackgroundScheduler()
            self.schedulers.start()
            self.schedulers.add_job(check_posts_date, 'cron', hour=12, minute=0)