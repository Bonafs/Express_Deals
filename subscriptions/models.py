"""
Express Deals - Subscription Management Models
Handle recurring payments, manual payments, and subscriptions with Stripe
"""

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from decimal import Decimal
import stripe
from django.conf import settings
from payments.models import StripeCustomer, SubscriptionPlan

# Set up Stripe with your live test key
stripe.api_key = settings.STRIPE_SECRET_KEY


class CustomerSubscription(models.Model):
    """Track customer subscriptions"""
    STATUS_CHOICES = [
        ('incomplete', 'Incomplete'),
        ('incomplete_expired', 'Incomplete Expired'),
        ('trialing', 'Trialing'),
        ('active', 'Active'),
        ('past_due', 'Past Due'),
        ('canceled', 'Canceled'),
        ('unpaid', 'Unpaid'),
    ]
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='customer_subscriptions'
    )
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE)
    stripe_subscription_id = models.CharField(max_length=100, unique=True)
    stripe_customer_id = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    current_period_start = models.DateTimeField()
    current_period_end = models.DateTimeField()
    trial_start = models.DateTimeField(null=True, blank=True)
    trial_end = models.DateTimeField(null=True, blank=True)
    canceled_at = models.DateTimeField(null=True, blank=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.plan.name} ({self.status})"
    
    def cancel_subscription(self, at_period_end=True):
        """Cancel the subscription"""
        try:
            stripe_subscription = stripe.Subscription.modify(
                self.stripe_subscription_id,
                cancel_at_period_end=at_period_end
            )
            
            if not at_period_end:
                self.status = 'canceled'
                self.canceled_at = timezone.now()
                self.ended_at = timezone.now()
            else:
                self.canceled_at = timezone.now()
            
            self.save()
            return stripe_subscription
        except stripe.error.StripeError as e:
            raise Exception(f"Stripe error: {e}")


class PaymentIntent(models.Model):
    """Track one-time manual payments"""
    STATUS_CHOICES = [
        ('requires_payment_method', 'Requires Payment Method'),
        ('requires_confirmation', 'Requires Confirmation'),
        ('requires_action', 'Requires Action'),
        ('processing', 'Processing'),
        ('requires_capture', 'Requires Capture'),
        ('canceled', 'Canceled'),
        ('succeeded', 'Succeeded'),
    ]
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='payment_intents'
    )
    stripe_payment_intent_id = models.CharField(max_length=100, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='gbp')
    status = models.CharField(max_length=30, choices=STATUS_CHOICES)
    description = models.TextField(blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    client_secret = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Payment £{self.amount} - {self.status}"
    
    @classmethod
    def create_payment_intent(cls, user, amount, description="", 
                              metadata=None):
        """Create a new payment intent"""
        try:
            stripe_intent = stripe.PaymentIntent.create(
                amount=int(amount * 100),  # Convert to pence
                currency='gbp',
                description=description,
                metadata=metadata or {},
                automatic_payment_methods={'enabled': True},
            )
            
            payment_intent = cls.objects.create(
                user=user,
                stripe_payment_intent_id=stripe_intent.id,
                amount=amount,
                status=stripe_intent.status,
                description=description,
                metadata=metadata or {},
                client_secret=stripe_intent.client_secret
            )
            
            return payment_intent
        except stripe.error.StripeError as e:
            raise Exception(f"Stripe error: {e}")


class PaymentHistory(models.Model):
    """Track all payment transactions"""
    PAYMENT_TYPES = [
        ('subscription', 'Subscription Payment'),
        ('one_time', 'One-time Payment'),
        ('refund', 'Refund'),
    ]
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscription_payment_history'
    )
    stripe_payment_id = models.CharField(max_length=100)
    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='gbp')
    status = models.CharField(max_length=20)
    description = models.TextField(blank=True)
    subscription = models.ForeignKey(
        CustomerSubscription,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    payment_intent = models.ForeignKey(
        PaymentIntent,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - £{self.amount} ({self.payment_type})"
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Payment History"