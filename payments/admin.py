from django.contrib import admin
from .models import Payment, Refund, StripeWebhookEvent

admin.site.register(Payment)
admin.site.register(Refund)
admin.site.register(StripeWebhookEvent)
from django.contrib import admin

# Register your models here.
