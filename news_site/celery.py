import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'news_site.settings')
app = Celery('news_site')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks()
