from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from orders.models import Order
import json
from django.db.models.signals import pre_save
from django.dispatch import receiver
from .utils import generate_payment_transaction_id


def generate_transaction_id():
    """Generate unique transaction ID"""
    from .utils import generate_payment_transaction_id
    return generate_payment_transaction_id()


class PaymentMethod(models.Model):
    """Store payment methods for users"""
    PAYMENT_TYPES = [
        ('credit_card', 'Credit Card'),
        ('debit_card', 'Debit Card'),
        ('paypal', 'PayPal'),
        ('stripe', 'Stripe'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payment_methods')
    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPES)
    
    # Credit Card Fields
    card_number = models.CharField(max_length=19, blank=True)  # Masked: **** **** **** 1234
    card_holder_name = models.CharField(max_length=100, blank=True)
    expiry_month = models.CharField(max_length=2, blank=True)
    expiry_year = models.CharField(max_length=4, blank=True)
    cvv = models.CharField(max_length=4, blank=True)
    
    # Stripe Fields
    stripe_customer_id = models.CharField(max_length=100, blank=True)
    stripe_payment_method_id = models.CharField(max_length=100, blank=True)
    
    # Demo Card Flag
    is_demo = models.BooleanField(default=False)
    
    is_default = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-is_default', '-created_at']
    
    def __str__(self):
        if self.payment_type == 'credit_card':
            return f"{self.card_holder_name} - {self.card_number}"
        return f"{self.user.username} - {self.get_payment_type_display()}"
    
    def mask_card_number(self):
        """Return masked card number"""
        if len(self.card_number) >= 4:
            return f"**** **** **** {self.card_number[-4:]}"
        return self.card_number


class Payment(models.Model):
    """Payment transaction records"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('succeeded', 'Succeeded'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded'),
    ]
    
    PAYMENT_TYPES = [
        ('one_time', 'One-time Payment'),
        ('subscription', 'Subscription Payment'),
        ('recurring', 'Recurring Payment'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='payments', null=True, blank=True)
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Payment Details
    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPES, default='one_time')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='GBP')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Stripe Integration
    stripe_payment_intent_id = models.CharField(max_length=100, blank=True)
    stripe_customer_id = models.CharField(max_length=100, blank=True)
    
    # Transaction Details
    transaction_id = models.CharField(max_length=100, unique=True, default=generate_transaction_id)
    gateway_response = models.JSONField(default=dict)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
@receiver(pre_save, sender=Payment)
def ensure_unique_transaction_id(sender, instance, **kwargs):
    if not instance.transaction_id or Payment.objects.filter(transaction_id=instance.transaction_id).exclude(pk=instance.pk).exists():
        new_id = generate_payment_transaction_id()
        while Payment.objects.filter(transaction_id=new_id).exists():
            new_id = generate_payment_transaction_id()
        instance.transaction_id = new_id
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Payment {self.transaction_id} - £{self.amount} ({self.status})"
    
    def mark_as_completed(self):
        """Mark payment as completed"""
        self.status = 'succeeded'
        self.completed_at = timezone.now()
        self.save()


class RecurringPayment(models.Model):
    """Recurring payment schedules"""
    FREQUENCY_CHOICES = [
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('yearly', 'Yearly'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('paused', 'Paused'),
        ('cancelled', 'Cancelled'),
        ('expired', 'Expired'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recurring_payments')
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE)
    
    # Subscription Details
    subscription_name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='GBP')
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES)
    
    # Schedule
    start_date = models.DateTimeField()
    next_payment_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True, blank=True)
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    
    # Stripe Integration
    stripe_subscription_id = models.CharField(max_length=100, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.subscription_name} - £{self.amount} {self.frequency}"


class SubscriptionPayment(models.Model):
    """Track subscription tier payments"""
    TIER_CHOICES = [
        ('free', 'Free'),
        ('basic', 'Basic'),
        ('premium', 'Premium'),
        ('vip', 'VIP'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscription_payments')
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name='subscription_details')
    recurring_payment = models.ForeignKey(RecurringPayment, on_delete=models.CASCADE, null=True, blank=True)
    
    # Subscription Details
    tier = models.CharField(max_length=20, choices=TIER_CHOICES)
    billing_period_start = models.DateTimeField()
    billing_period_end = models.DateTimeField()
    
    # Features
    max_alerts = models.IntegerField(default=0)
    max_wishlists = models.IntegerField(default=0)
    priority_support = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.tier.title()} Subscription"


class DemoCard(models.Model):
    """Demo credit cards for testing"""
    CARD_TYPES = [
        ('visa', 'Visa'),
        ('mastercard', 'Mastercard'),
        ('amex', 'American Express'),
        ('discover', 'Discover'),
    ]
    
    card_type = models.CharField(max_length=20, choices=CARD_TYPES)
    card_number = models.CharField(max_length=19)
    card_holder_name = models.CharField(max_length=100)
    expiry_month = models.CharField(max_length=2)
    expiry_year = models.CharField(max_length=4)
    cvv = models.CharField(max_length=4)
    
    # Test scenarios
    scenario = models.CharField(max_length=100, help_text="e.g., 'Success', 'Declined', 'Insufficient Funds'")
    description = models.TextField(blank=True)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['card_type', 'scenario']
    
    def __str__(self):
        return f"{self.card_type.title()} - {self.scenario} - {self.card_number}"


class StripeWebhookEvent(models.Model):
    """Track Stripe webhook events"""
    stripe_event_id = models.CharField(max_length=100, unique=True)
    event_type = models.CharField(max_length=50)
    data = models.JSONField()
    processed = models.BooleanField(default=False)
    processed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Webhook {self.event_type} - {self.stripe_event_id}"
