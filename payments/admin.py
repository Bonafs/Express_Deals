from django.contrib import admin
from .models import Payment, StripeWebhookEvent

admin.site.register(Payment)
admin.site.register(StripeWebhookEvent)
from django.contrib import admin

# Register your models here.
