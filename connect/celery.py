from __future__ import absolute_import, unicode_literals
import os
import sys

from celery import Celery, schedules

from connect import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "connect.settings")

app = Celery("connect")
app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.conf.beat_schedule = {
    "check-status-services": {
        "task": "connect.common.tasks.status_service",
        "schedule": schedules.crontab(minute="*/3"),
    },
    "delete-status-logs": {
        "task": "connect.common.tasks.delete_status_logs",
        "schedule": schedules.crontab(hour="22", minute=0),
    },
    "check-organization-free-plan": {
        "task": "connect.common.tasks.check_organization_free_plan",
        "schedule": schedules.crontab(minute="*/6"),
    },
    "sync-project-information": {
        "task": "connect.common.tasks.sync_project_information",
        "schedule": schedules.crontab(minute="*/5")
    },
    "sync-project-statistics": {
        "task": "connect.common.tasks.sync_project_statistics",
        "schedule": schedules.crontab(minute="*/6")
    },
    "sync-repositories-statistics": {
        "task": "connect.common.tasks.sync_repositories_statistics",
        "schedule": schedules.crontab(minute="*/8")
    },
    "sync-channels-statistics": {
        "task": "connect.common.tasks.sync_channels_statistics",
        "schedule": schedules.crontab(minute="*/7")
    },
    "generate_project_invoice": {
        "task": "connect.common.tasks.generate_project_invoice",
        "schedule": schedules.crontab(minute="*/5"),
    },
    "sync-total-active-contacts": {
        "task": "connect.common.tasks.sync_total_contact_count",
        "schedule": schedules.crontab(hour="3", minute=0)
    },
    "sync-active-contacts": {
        "task": "connect.common.tasks.sync_active_contacts",
        "schedule": schedules.crontab(hour="*/6")
    },
    "capture_invoice": {
        "task": "connect.common.tasks.capture_invoice",
        "schedule": schedules.crontab(hour="8,10,13,15,17", minute=0),
        # "schedule": 30,
    }
}


@app.task(bind=True)
def debug_task(self):
    print("Request: {0!r}".format(self.request))


if "test" in sys.argv or getattr(settings, "CELERY_ALWAYS_EAGER", False):
    from celery import current_app

    def send_task(name, args=(), kwargs={}, **opts):  # pragma: needs cover
        task = current_app.tasks[name]
        return task.apply(args, kwargs, **opts)

    current_app.send_task = send_task
