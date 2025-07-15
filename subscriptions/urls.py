"""
Express Deals - Subscription and Payment URLs
URL routing for recurring payments, manual payments, and subscriptions
"""

from django.urls import path
from . import views

app_name = 'subscriptions'

urlpatterns = [
    # Subscription Management
    path('plans/', views.subscription_plans, name='plans'),
    path('create/', views.create_subscription, name='create_subscription'),
    path('management/', views.subscription_management, name='management'),
    path('cancel/', views.cancel_subscription, name='cancel_subscription'),
    
    # Manual Payments
    path('payment/', views.manual_payment, name='manual_payment'),
    path('payment/create-intent/', views.create_payment_intent, name='create_payment_intent'),
    path('payment/success/', views.payment_success, name='payment_success'),
    
    # Webhooks
    path('webhook/stripe/', views.stripe_webhook, name='stripe_webhook'),
]
