from celery import Celery

from application import create_app

# -------------------------------------------------------------------
# Flask Application
# -------------------------------------------------------------------

app = create_app()

# -------------------------------------------------------------------
# Celery Configuration
# -------------------------------------------------------------------

celery = Celery(
    "trekking_app",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0",
)

celery.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="Asia/Kolkata",
    enable_utc=True,
)

# -------------------------------------------------------------------
# Flask Application Context for Celery Tasks
# -------------------------------------------------------------------

class ContextTask(celery.Task):
    def __call__(self, *args, **kwargs):
        with app.app_context():
            return self.run(*args, **kwargs)


celery.Task = ContextTask

# -------------------------------------------------------------------
# Register Celery Tasks
# -------------------------------------------------------------------

import application.tasks