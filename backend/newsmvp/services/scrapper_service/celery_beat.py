from celery import Celery
from celery.schedules import crontab

from core.config import settings

celery_app = Celery(
    main="tasks_service",
    broker=settings.broker_url,
    backend=settings.result_backend_url,
    include=["services.scrapper_service.celery_worker"],
)

celery_app.conf.timezone = "UTC"
celery_app.conf.beat_schedule_filename = "celerybeat-schedule/"

celery_app.conf.beat_schedule = {
    "rss_parser_news": {
        "task": "services.scrapper_service.celery_worker.run_full_parse_pipeline",
        "schedule": crontab(
            minute="*/2",
        ),  # hour="*/1"),
        # ),  # hour="*/1"),
    },
    # "cluster_news": {
    #     "task": "services.scrapper_service.celery_worker.run_clusterization",
    #     "schedule": crontab(minute=0, hour="*/3"),
    # },
}
