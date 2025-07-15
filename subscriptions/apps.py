from django.apps import AppConfig


class SubscriptionsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'subscriptions'
    verbose_name = 'Subscription Management'

    def ready(self):
        # Import signal handlers
        try:
            import subscriptions.signals
        except ImportError:
            pass
