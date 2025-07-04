from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import UserProfile


class UserProfileInline(admin.StackedInline):
    """
    Inline admin for UserProfile
    """
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile Information'
    
    fieldsets = (
        ('Contact Information', {
            'fields': ('phone_number', 'whatsapp_number')
        }),
        ('Notification Preferences', {
            'fields': ('email_notifications_enabled', 'sms_notifications_enabled', 
                      'whatsapp_notifications_enabled', 'push_notifications_enabled')
        }),
        ('Alert Preferences', {
            'fields': ('price_alert_threshold', 'deal_categories')
        }),
        ('Address Information', {
            'fields': ('address', 'city', 'state', 'zip_code', 'country'),
            'classes': ('collapse',)
        }),
        ('Personal Information', {
            'fields': ('date_of_birth', 'preferred_currency', 'timezone'),
            'classes': ('collapse',)
        })
    )


class UserAdmin(BaseUserAdmin):
    """
    Extended User admin with profile inline
    """
    inlines = (UserProfileInline,)
    
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 
                   'get_whatsapp_number', 'get_whatsapp_enabled')
    list_filter = BaseUserAdmin.list_filter + ('profile__whatsapp_notifications_enabled',)
    
    def get_whatsapp_number(self, obj):
        return obj.profile.whatsapp_number if hasattr(obj, 'profile') else '-'
    get_whatsapp_number.short_description = 'WhatsApp Number'
    
    def get_whatsapp_enabled(self, obj):
        return obj.profile.whatsapp_notifications_enabled if hasattr(obj, 'profile') else False
    get_whatsapp_enabled.short_description = 'WhatsApp Enabled'
    get_whatsapp_enabled.boolean = True


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """
    Admin interface for UserProfile
    """
    list_display = ('user', 'phone_number', 'whatsapp_number', 'email_notifications_enabled',
                   'sms_notifications_enabled', 'whatsapp_notifications_enabled', 'created_at')
    list_filter = ('email_notifications_enabled', 'sms_notifications_enabled', 
                  'whatsapp_notifications_enabled', 'created_at')
    search_fields = ('user__username', 'user__email', 'phone_number', 'whatsapp_number')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Contact Information', {
            'fields': ('phone_number', 'whatsapp_number')
        }),
        ('Notification Preferences', {
            'fields': ('email_notifications_enabled', 'sms_notifications_enabled',
                      'whatsapp_notifications_enabled', 'push_notifications_enabled')
        }),
        ('Alert Preferences', {
            'fields': ('price_alert_threshold', 'deal_categories')
        }),
        ('Address Information', {
            'fields': ('address', 'city', 'state', 'zip_code', 'country'),
            'classes': ('collapse',)
        }),
        ('Personal Information', {
            'fields': ('date_of_birth', 'preferred_currency', 'timezone'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    actions = ['enable_whatsapp_notifications', 'disable_whatsapp_notifications']
    
    def enable_whatsapp_notifications(self, request, queryset):
        """Enable WhatsApp notifications for selected users"""
        updated = queryset.update(whatsapp_notifications_enabled=True)
        self.message_user(request, f'WhatsApp notifications enabled for {updated} users.')
    enable_whatsapp_notifications.short_description = 'Enable WhatsApp notifications'
    
    def disable_whatsapp_notifications(self, request, queryset):
        """Disable WhatsApp notifications for selected users"""
        updated = queryset.update(whatsapp_notifications_enabled=False)
        self.message_user(request, f'WhatsApp notifications disabled for {updated} users.')
    disable_whatsapp_notifications.short_description = 'Disable WhatsApp notifications'


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
