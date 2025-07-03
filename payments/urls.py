from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    # Payment processing
    path('payment/<int:order_id>/', views.PaymentView.as_view(), name='payment'),
    path('success/', views.PaymentSuccessView.as_view(), name='payment_success'),
    path('cancel/', views.PaymentCancelView.as_view(), name='payment_cancel'),
    
    # Webhooks
    path('webhook/stripe/', views.StripeWebhookView.as_view(), name='stripe_webhook'),
    
    # Refunds (admin only)
    path('refund/<int:order_id>/', views.RefundView.as_view(), name='refund'),
    
    # Legacy URLs for backward compatibility
    path('process/', views.PaymentView.as_view(), name='process_payment'),
]
