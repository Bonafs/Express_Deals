"""
Express Deals - Celery Configuration
Background task processing for scraping and price monitoring
"""

from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'express_deals.settings')

app = Celery('express_deals')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

# Celery Beat Schedule for periodic tasks
from celery.schedules import crontab

app.conf.beat_schedule = {
    # Run price checks every 5 minutes
    'check-price-alerts': {
        'task': 'scraping.tasks.check_price_alerts',
        'schedule': 300.0,  # 5 minutes
    },
    # Scrape new products every hour
    'scrape-products': {
        'task': 'scraping.tasks.scrape_all_targets',
        'schedule': 3600.0,  # 1 hour
    },
    # Send notification digest every 6 hours
    'send-notification-digest': {
        'task': 'scraping.tasks.send_notification_digest',
        'schedule': 21600.0,  # 6 hours
    },
    # Cleanup old data daily at 2 AM
    'cleanup-old-data': {
        'task': 'scraping.tasks.cleanup_old_data',
        'schedule': crontab(hour=2, minute=0),
    },
    # Update trending deals every 30 minutes
    'update-trending-deals': {
        'task': 'scraping.tasks.update_trending_deals',
        'schedule': 1800.0,  # 30 minutes
    },
    # Monitor scrape job health every 15 minutes
    'monitor-scrape-jobs': {
        'task': 'scraping.tasks.monitor_scrape_jobs',
        'schedule': 900.0,  # 15 minutes
    },
}

# Enhanced Celery Configuration
app.conf.update(
    # Time zone for scheduling
    timezone='UTC',
    
    # Task serialization
    task_serializer='json',
    result_serializer='json',
    accept_content=['json'],
    
    # Task routing
    task_routes={
        'scraping.tasks.scrape_product': {'queue': 'scraping'},
        'scraping.tasks.check_price_alerts': {'queue': 'alerts'},
        'scraping.tasks.send_notification': {'queue': 'notifications'},
        'scraping.tasks.send_email_notification': {'queue': 'notifications'},
        'scraping.tasks.send_sms_notification': {'queue': 'notifications'},
    },
    
    # Worker configuration
    worker_prefetch_multiplier=1,
    task_acks_late=True,
    
    # Result backend configuration
    result_expires=3600,  # 1 hour
    
    # Task retry configuration
    task_default_retry_delay=60,  # 1 minute
    task_max_retries=3,
    
    # Rate limiting
    task_annotations={
        'scraping.tasks.scrape_product': {'rate_limit': '10/m'},
        'scraping.tasks.send_sms_notification': {'rate_limit': '50/m'},
        'scraping.tasks.send_email_notification': {'rate_limit': '100/m'},
    },
)

@app.task(bind=True)
def debug_task(self):
    """Debug task to test Celery functionality."""
    print(f'Request: {self.request!r}')
    return 'Debug task completed successfully'
