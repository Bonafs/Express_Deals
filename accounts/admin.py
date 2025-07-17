Django """
Enhanced Django Admin Configuration for Express Deals User Management

This module provides a production-ready admin interface with:
- Reusable fieldset mixins for DRY configuration
- Enhanced User admin with profile integration and analytics
- Advanced UserProfile admin with CSV export and bulk actions
- Multi-region support with currency and timezone filtering
- Improved UX with emoji indicators and detailed feedback
- Automatic profile creation and readonly permissions handling

Author: Express Deals Team
Version: 2.0 - Production Ready
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.utils.html import format_html
import csv
from .models import UserProfile


# Reusable fieldset helper for DRY admin configuration
class BaseProfileFieldsetsMixin:
    """
    Mixin providing reusable fieldset configurations for profile-related admin classes
    """
    @staticmethod
    def get_contact_fieldset():
        return ('Contact Information', {
            'fields': ('phone_number', 'whatsapp_number')
        })
    
    @staticmethod
    def get_notification_fieldset():
        return ('Notification Preferences', {
            'fields': ('email_notifications_enabled', 'sms_notifications_enabled', 
                      'whatsapp_notifications_enabled', 'push_notifications_enabled')
        })
    
    @staticmethod
    def get_alert_fieldset():
        return ('Alert Preferences', {
            'fields': ('price_alert_threshold', 'deal_categories')
        })
    
    @staticmethod
    def get_address_fieldset():
        return ('Address Information', {
            'fields': ('address', 'city', 'county', 'postcode', 'country'),
            'classes': ('collapse',)
        })
    
    @staticmethod
    def get_personal_fieldset():
        return ('Personal Information', {
            'fields': ('date_of_birth', 'preferred_currency', 'timezone'),
            'classes': ('collapse',)
        })


class UserProfileInline(admin.StackedInline, BaseProfileFieldsetsMixin):
    """
    Inline admin for UserProfile with improved UX
    """
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile Information'
    
    @property
    def fieldsets(self):
        return (
            self.get_contact_fieldset(),
            self.get_notification_fieldset(),
            self.get_alert_fieldset(),
            self.get_address_fieldset(),
            self.get_personal_fieldset(),
        )


class UserProfileReadOnlyInline(admin.StackedInline):
    """
    Readonly inline for users without edit permissions
    """
    model = UserProfile
    can_delete = False
    extra = 0
    readonly_fields = ('phone_number', 'whatsapp_number', 'email_notifications_enabled',
                       'sms_notifications_enabled', 'whatsapp_notifications_enabled',
                       'preferred_currency', 'timezone', 'created_at')
    fields = readonly_fields
    verbose_name_plural = 'Profile Information (Read Only)'
    
    def has_add_permission(self, request, obj=None):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False


class UserAdmin(BaseUserAdmin):
    """
    Extended User admin with enhanced profile integration and analytics
    """
    inlines = (UserProfileInline,)
    
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff',
                    'get_whatsapp_number', 'get_whatsapp_enabled', 'get_currency',
                    'get_timezone')
    list_filter = (BaseUserAdmin.list_filter + 
                   ('profile__whatsapp_notifications_enabled',
                    'profile__preferred_currency', 'profile__timezone'))
    autocomplete_fields = []  # Ready for future foreign key relationships
    
    def get_whatsapp_number(self, obj):
        """Get WhatsApp number with improved error handling"""
        profile = getattr(obj, 'profile', None)
        return profile.whatsapp_number if profile else '-'
    get_whatsapp_number.short_description = 'WhatsApp Number'
    
    def get_whatsapp_enabled(self, obj):
        """Check if WhatsApp notifications are enabled"""
        profile = getattr(obj, 'profile', None)
        return profile.whatsapp_notifications_enabled if profile else False
    get_whatsapp_enabled.short_description = 'WhatsApp Enabled'
    get_whatsapp_enabled.boolean = True
    
    def get_currency(self, obj):
        """Get user's preferred currency"""
        profile = getattr(obj, 'profile', None)
        return profile.preferred_currency if profile else 'GBP'
    get_currency.short_description = 'Currency'
    
    def get_timezone(self, obj):
        """Get user's timezone"""
        profile = getattr(obj, 'profile', None)
        return profile.timezone if profile else 'Europe/London'
    get_timezone.short_description = 'Timezone'
    
    def save_model(self, request, obj, form, change):
        """Ensure UserProfile is created when User is saved"""
        super().save_model(request, obj, form, change)
        if not hasattr(obj, 'profile'):
            UserProfile.objects.create(user=obj)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin, BaseProfileFieldsetsMixin):
    """
    Enhanced admin interface for UserProfile with analytics and export capabilities
    """
    list_display = ('user', 'phone_number', 'whatsapp_number', 
                    'email_notifications_enabled', 'sms_notifications_enabled',
                    'whatsapp_notifications_enabled', 'get_currency_display',
                    'created_at')
    list_filter = ('email_notifications_enabled', 'sms_notifications_enabled',
                   'whatsapp_notifications_enabled', 'preferred_currency',
                   'timezone', 'created_at')
    search_fields = ('user__username', 'user__email', 'phone_number',
                     'whatsapp_number', 'user__first_name', 'user__last_name')
    readonly_fields = ('created_at', 'updated_at')
    autocomplete_fields = ['user']  # Enable autocomplete for User selection
    
    @property
    def fieldsets(self):
        return (
            ('User Information', {
                'fields': ('user',)
            }),
            self.get_contact_fieldset(),
            self.get_notification_fieldset(),
            self.get_alert_fieldset(),
            self.get_address_fieldset(),
            self.get_personal_fieldset(),
            ('Timestamps', {
                'fields': ('created_at', 'updated_at'),
                'classes': ('collapse',)
            })
        )
    
    actions = ['enable_whatsapp_notifications', 'disable_whatsapp_notifications',
               'export_profiles_csv', 'enable_all_notifications',
               'disable_all_notifications']
    
    def get_currency_display(self, obj):
        """Display currency with flag emoji for better UX"""
        currency_flags = {
            'GBP': '🇬🇧', 'USD': '🇺🇸', 'EUR': '🇪🇺',
            'CAD': '🇨🇦', 'AUD': '🇦🇺'
        }
        flag = currency_flags.get(obj.preferred_currency, '💱')
        return format_html(f'{flag} {obj.preferred_currency}')
    get_currency_display.short_description = 'Currency'
    
    def enable_whatsapp_notifications(self, request, queryset):
        """Enable WhatsApp notifications with detailed feedback"""
        updated = queryset.update(whatsapp_notifications_enabled=True)
        usernames = list(queryset.values_list('user__username', flat=True))
        self.message_user(
            request,
            f'WhatsApp notifications enabled for {updated} users: '
            f'{", ".join(usernames[:5])}'
            f'{"..." if len(usernames) > 5 else ""}'
        )
    enable_whatsapp_notifications.short_description = 'Enable WhatsApp notifications'
    
    def disable_whatsapp_notifications(self, request, queryset):
        """Disable WhatsApp notifications with detailed feedback"""
        updated = queryset.update(whatsapp_notifications_enabled=False)
        usernames = list(queryset.values_list('user__username', flat=True))
        self.message_user(
            request,
            f'WhatsApp notifications disabled for {updated} users: '
            f'{", ".join(usernames[:5])}'
            f'{"..." if len(usernames) > 5 else ""}'
        )
    disable_whatsapp_notifications.short_description = 'Disable WhatsApp notifications'
    
    def enable_all_notifications(self, request, queryset):
        """Enable all notification types for selected users"""
        updated = queryset.update(
            email_notifications_enabled=True,
            sms_notifications_enabled=True,
            whatsapp_notifications_enabled=True,
            push_notifications_enabled=True
        )
        self.message_user(
            request,
            f'All notifications enabled for {updated} users.'
        )
    enable_all_notifications.short_description = 'Enable all notifications'
    
    def disable_all_notifications(self, request, queryset):
        """Disable all notification types for selected users"""
        updated = queryset.update(
            email_notifications_enabled=False,
            sms_notifications_enabled=False,
            whatsapp_notifications_enabled=False,
            push_notifications_enabled=False
        )
        self.message_user(
            request,
            f'All notifications disabled for {updated} users.'
        )
    disable_all_notifications.short_description = 'Disable all notifications'
    
    def export_profiles_csv(self, request, queryset):
        """Export selected user profiles to CSV for analytics"""
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="user_profiles.csv"'
        
        writer = csv.writer(response)
        writer.writerow([
            'Username', 'Email', 'Full Name', 'Phone', 'WhatsApp',
            'Email Notifications', 'SMS Notifications', 'WhatsApp Notifications',
            'Currency', 'Timezone', 'City', 'Country', 'Created'
        ])
        
        for profile in queryset.select_related('user'):
            writer.writerow([
                profile.user.username,
                profile.user.email,
                profile.full_name,
                profile.phone_number or '',
                profile.whatsapp_number or '',
                'Yes' if profile.email_notifications_enabled else 'No',
                'Yes' if profile.sms_notifications_enabled else 'No',
                'Yes' if profile.whatsapp_notifications_enabled else 'No',
                profile.preferred_currency,
                profile.timezone,
                profile.city or '',
                profile.country,
                profile.created_at.strftime('%Y-%m-%d')
            ])
        
        self.message_user(
            request,
            f'Exported {queryset.count()} user profiles to CSV.'
        )
        return response
    export_profiles_csv.short_description = 'Export to CSV'


class UserProfileReadOnlyInline(admin.StackedInline):
    """
    Readonly inline for users without edit permissions
    """
    model = UserProfile
    can_delete = False
    extra = 0
    readonly_fields = ('phone_number', 'whatsapp_number', 'email_notifications_enabled',
                       'sms_notifications_enabled', 'whatsapp_notifications_enabled',
                       'preferred_currency', 'timezone', 'created_at')
    fields = readonly_fields
    verbose_name_plural = 'Profile Information (Read Only)'
    
    def has_add_permission(self, request, obj=None):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False


# Re-register UserAdmin with enhanced functionality
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
