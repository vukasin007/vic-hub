# independent file

import os

from celery import Celery, shared_task
from celery.schedules import crontab
from celery.utils.log import get_task_logger
# vukasin007

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'VicHub.settings')

app = Celery('VicHub')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')


app.conf.update(
    result_expires=3600,
)


# @app.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):
#     # Calls test('hello') every 10 seconds.
#     sender.add_periodic_task(10.0, test.s('hello'), name='add every 10')
#
#     # Calls test('hello') every 10 seconds.
#     sender.add_periodic_task(2.0, tick.s(), name='tick called')
#
#     # Calls test('world') every 30 seconds
#     sender.add_periodic_task(30.0, test.s('world'), expires=10)
#
#     # Executes every Monday morning at 7:30 a.m.
#     sender.add_periodic_task(
#         crontab(hour=7, minute=30, day_of_week=1),
#         test.s('Happy Mondays!'),
#     )

app.conf.beat_schedule = {
    # 'tick-every-2-seconds': {
    #     'task': 'tick',
    #     'schedule': 2.0,
    # },
    'send-emails-on-bilten': {
        'task': 'send-mail-function',
        # 'schedule': crontab(hour=10, minute=00, day_of_week=7),
        'schedule': 10.0,
    }
}


if __name__ == '__main__':
    app.start()
