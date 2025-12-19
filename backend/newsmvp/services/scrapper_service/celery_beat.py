from datetime import datetime
from celery import Celery
from celery.schedules import crontab

from core.config import settings

celery_app = Celery(
    main="tasks_service",
    broker=settings.redis_url,
    backend=settings.redis_url,
    include=["services.scrapper_service.celery_worker"],
)

celery_app.conf.beat_schedule = {
    "rss_parser_news": {
        "task": "services.scrapper_service.celery_worker.execute_parser_rss",
        "schedule": crontab(minute="*/1"),
    },
}

celery_app.conf.timezone = "UTC"

# @app.task
# def hello():
#     return "hello world"
#
#
# @app.task
# def generate_report():
#     print(f"Published: {datetime.now()}")
#
#
# generate_report.apply_async(countdown=2)
