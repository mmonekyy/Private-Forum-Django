from django.apps import AppConfig
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler import schedulers
import os
def check_posts_date():
    from forum_register.models import User_gen_kay
    from django.utils import timezone
    print('Checking Keys date...')
    curent_time = timezone.now()
    User_gen_kay.objects.filter(next_key__lt=curent_time).delete()
    

class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'forum_users'

    def ready(self):
        if os.environ.get('RUN_MAIN', None) != 'true':
            return
        print('## Starting scheduler for checking Keys ... ##')
        self.schedulers = BackgroundScheduler()
        self.schedulers.start()
        self.schedulers.add_job(check_posts_date, 'cron', hour=12, minute=0)