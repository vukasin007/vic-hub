# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.

# ---------- for celery ------------
from .celery import app as celery_app
# vukasin007

__all__ = ('celery_app',)
# ----------------------------------
