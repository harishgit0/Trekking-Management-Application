from celery import Celery
from celery.schedules import crontab
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

    beat_schedule={

        # Daily Reminder
        "daily-trek-reminder": {
            "task": "application.tasks.daily_reminder_task",
            "schedule": crontab(),   # 6:00 PM daily
        },

        # Monthly Activity Report
        "monthly-admin-report": {
            "task": "application.tasks.monthly_report_task",
            "schedule": crontab(),  # 1st day of every month
        },
    },
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