"""
Express Deals - Notification Service
Unified notification system for alerts and communications
"""

from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import logging

logger = logging.getLogger(__name__)


class NotificationService:
    """
    Centralized service for sending notifications via multiple channels
    """
    
    def __init__(self):
        self.email_enabled = hasattr(settings, 'EMAIL_HOST')
        self.sms_enabled = hasattr(settings, 'TWILIO_ACCOUNT_SID')
        self.push_enabled = False  # TODO: Implement push notifications
    
    def send_price_alert(self, user, product, alert_type, price_info):
        """
        Send a price alert notification
        """
        context = {
            'user': user,
            'product': product,
            'alert_type': alert_type,
            'price_info': price_info,
            'site_url': getattr(settings, 'SITE_URL', 'http://localhost:8000'),
        }
        
        # Send email if enabled
        if self.email_enabled and user.email:
            self.send_email_notification(
                user.email,
                'price_alert',
                context
            )
        
        # Send SMS if enabled and user has phone number
        if self.sms_enabled and hasattr(user, 'profile') and user.profile.phone_number:
            self.send_sms_notification(
                user.profile.phone_number,
                'price_alert',
                context
            )
    
    def send_email_notification(self, recipient_email, template_name, context):
        """
        Send email notification using Django templates
        """
        try:
            subject_template = f'emails/{template_name}_subject.txt'
            html_template = f'emails/{template_name}.html'
            text_template = f'emails/{template_name}.txt'
            
            # Render templates
            subject = render_to_string(subject_template, context).strip()
            html_message = render_to_string(html_template, context)
            text_message = render_to_string(text_template, context)
            
            # Send email
            send_mail(
                subject=subject,
                message=text_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[recipient_email],
                html_message=html_message,
                fail_silently=False,
            )
            
            logger.info(f"Email notification sent to {recipient_email}")
            return True
        
        except Exception as e:
            logger.error(f"Failed to send email notification: {e}")
            return False
    
    def send_sms_notification(self, phone_number, template_name, context):
        """
        Send SMS notification using Twilio
        """
        try:
            from twilio.rest import Client
            
            # Initialize Twilio client
            client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
            
            # Render SMS message template
            sms_template = f'sms/{template_name}.txt'
            message = render_to_string(sms_template, context).strip()
            
            # Send SMS
            twilio_message = client.messages.create(
                body=message,
                from_=settings.TWILIO_PHONE_NUMBER,
                to=phone_number
            )
            
            logger.info(f"SMS notification sent to {phone_number}")
            return True
        
        except Exception as e:
            logger.error(f"Failed to send SMS notification: {e}")
            return False
    
    def send_deal_alert(self, user, deals):
        """
        Send a deal alert with multiple products
        """
        context = {
            'user': user,
            'deals': deals,
            'site_url': getattr(settings, 'SITE_URL', 'http://localhost:8000'),
        }
        
        if self.email_enabled and user.email:
            self.send_email_notification(
                user.email,
                'deal_alert',
                context
            )
    
    def send_welcome_email(self, user):
        """
        Send welcome email to new users
        """
        context = {
            'user': user,
            'site_url': getattr(settings, 'SITE_URL', 'http://localhost:8000'),
        }
        
        if self.email_enabled and user.email:
            self.send_email_notification(
                user.email,
                'welcome',
                context
            )
    
    def send_order_confirmation(self, order):
        """
        Send order confirmation email
        """
        context = {
            'order': order,
            'user': order.user,
            'site_url': getattr(settings, 'SITE_URL', 'http://localhost:8000'),
        }
        
        if self.email_enabled and order.user.email:
            self.send_email_notification(
                order.user.email,
                'order_confirmation',
                context
            )
