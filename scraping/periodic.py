# Auto-create a periodic task for scraping all active targets every hour
from django_celery_beat.models import PeriodicTask, IntervalSchedule
from django.apps import apps

def setup_scraping_periodic_task():
    # Avoid duplicate tasks
    if not PeriodicTask.objects.filter(task='scraping.tasks.scrape_all_active_targets').exists():
        schedule, _ = IntervalSchedule.objects.get_or_create(every=1, period=IntervalSchedule.HOURS)
        PeriodicTask.objects.create(
            interval=schedule,
            name='Scrape All Active Targets Every Hour',
            task='scraping.tasks.scrape_all_active_targets',
            enabled=True
        )

def ready_hook():
    # Only run in main process
    if apps.is_installed('django_celery_beat'):
        setup_scraping_periodic_task()
