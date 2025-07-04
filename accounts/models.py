from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    """
    Extended user profile with additional fields for notifications
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    # Contact Information
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    whatsapp_number = models.CharField(max_length=20, blank=True, null=True)
    
    # Notification Preferences
    email_notifications_enabled = models.BooleanField(default=True)
    sms_notifications_enabled = models.BooleanField(default=False)
    whatsapp_notifications_enabled = models.BooleanField(default=False)
    push_notifications_enabled = models.BooleanField(default=True)
    
    # Alert Preferences
    price_alert_threshold = models.DecimalField(max_digits=5, decimal_places=0, default=10, 
                                               help_text="Minimum discount percentage for alerts")
    deal_categories = models.JSONField(default=list, blank=True,
                                     help_text="Preferred product categories for deals")
    
    # Profile Information
    date_of_birth = models.DateField(blank=True, null=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    zip_code = models.CharField(max_length=10, blank=True)
    country = models.CharField(max_length=100, default='United States')
    
    # Preferences
    preferred_currency = models.CharField(max_length=3, default='USD')
    timezone = models.CharField(max_length=50, default='UTC')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'user_profiles'
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'
    
    def __str__(self):
        return f"{self.user.username}'s Profile"
    
    @property
    def full_name(self):
        return f"{self.user.first_name} {self.user.last_name}".strip()
    
    @property
    def has_whatsapp(self):
        return bool(self.whatsapp_number and self.whatsapp_notifications_enabled)
    
    @property
    def has_sms(self):
        return bool(self.phone_number and self.sms_notifications_enabled)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Create user profile when user is created
    """
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Save user profile when user is saved
    """
    if hasattr(instance, 'profile'):
        instance.profile.save()
    else:
        UserProfile.objects.create(user=instance)
