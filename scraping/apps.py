"""
Express Deals - Scraping App Configuration
"""

from django.apps import AppConfig


class ScrapingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'scraping'
    verbose_name = 'Web Scraping & Price Monitoring'
    
    def ready(self):
        """
        Initialize app when Django starts
        """
        # Import signal handlers
        try:
            from . import signals
        except ImportError:
            pass
