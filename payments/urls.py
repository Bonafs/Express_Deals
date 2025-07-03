from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('process/', views.ProcessPaymentView.as_view(), name='process_payment'),
    path('success/', views.PaymentSuccessView.as_view(), name='payment_success'),
    path('cancel/', views.PaymentCancelView.as_view(), name='payment_cancel'),
    path('webhook/', views.StripeWebhookView.as_view(), name='stripe_webhook'),
]
