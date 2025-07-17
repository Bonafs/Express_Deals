from django.db import models
from django.contrib.auth.models import User
from products.models import Product
from payments.models import SubscriptionPlan


class DealCategory(models.Model):
    """Categories for organizing deals and price alerts"""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Deal Categories'
        ordering = ['name']

    def __str__(self):
        return self.name


class UserSubscription(models.Model):
    """User subscription to premium deal hunting plans"""
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='subscription'
    )
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    started_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    auto_renew = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.plan.display_name}"


class PriceAlert(models.Model):
    """Price and availability alerts for products"""
    ALERT_TYPES = [
        ('price_drop', 'Price Drop'),
        ('stock_available', 'Back in Stock'),
        ('deal_category', 'Category Deal'),
    ]
    
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='price_alerts'
    )
    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True
    )
    category = models.ForeignKey(
        DealCategory, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True
    )
    alert_type = models.CharField(max_length=20, choices=ALERT_TYPES)
    target_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        null=True, 
        blank=True
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        if self.product:
            return f"{self.user.username} - {self.product.name} alert"
        return f"{self.user.username} - {self.category.name} category alert"


class AlertNotification(models.Model):
    """Notification history for price alerts"""
    NOTIFICATION_TYPES = [
        ('email', 'Email'),
        ('sms', 'SMS'),
        ('push', 'Push Notification'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('sent', 'Sent'),
        ('failed', 'Failed'),
    ]
    
    alert = models.ForeignKey(
        PriceAlert, 
        on_delete=models.CASCADE, 
        related_name='notifications'
    )
    notification_type = models.CharField(
        max_length=10, 
        choices=NOTIFICATION_TYPES
    )
    status = models.CharField(
        max_length=10, 
        choices=STATUS_CHOICES, 
        default='pending'
    )
    message = models.TextField()
    sent_at = models.DateTimeField(null=True, blank=True)
    error_message = models.TextField(blank=True)
    
    def __str__(self):
        return (f"{self.alert.user.username} - {self.notification_type} - "
                f"{self.status}")
