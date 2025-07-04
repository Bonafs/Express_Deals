"""
Express Deals - Notification Service
Unified notification system for alerts and communications
"""

from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import logging
import requests

logger = logging.getLogger(__name__)


class NotificationService:
    """
    Centralized service for sending notifications via multiple channels
    """
    
    def __init__(self):
        self.email_enabled = hasattr(settings, 'EMAIL_HOST')
        self.sms_enabled = hasattr(settings, 'TWILIO_ACCOUNT_SID')
        self.whatsapp_enabled = getattr(settings, 'WHATSAPP_ENABLED', False)
        self.push_enabled = False
    
    def send_price_alert(self, user, product, alert_type, price_info):
        """Send a price alert notification"""
        context = {
            'user': user,
            'product': product,
            'alert_type': alert_type,
            'price_info': price_info,
            'site_url': getattr(settings, 'SITE_URL', 'http://localhost:8000'),
        }
        
        if self.email_enabled and user.email:
            self.send_email_notification(user.email, 'price_alert', context)
        
        if self.sms_enabled and hasattr(user, 'profile') and user.profile.phone_number:
            self.send_sms_notification(user.profile.phone_number, 'price_alert', context)
        
        if self.whatsapp_enabled and hasattr(user, 'profile') and user.profile.whatsapp_number:
            self.send_whatsapp_notification(user.profile.whatsapp_number, 'price_alert', context)
    
    def send_email_notification(self, email, template_name, context):
        """Send email notification"""
        try:
            subject = self._get_default_subject(template_name, context)
            body = self._get_default_body(template_name, context)
            
            send_mail(
                subject=subject,
                message=body,
                from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@expressdeals.com'),
                recipient_list=[email],
                fail_silently=False
            )
            
            logger.info(f"Email sent successfully to {email}")
            
        except Exception as e:
            logger.error(f"Failed to send email to {email}: {e}")
    
    def send_sms_notification(self, phone_number, template_name, context):
        """Send SMS notification via Twilio"""
        try:
            from twilio.rest import Client
            
            account_sid = getattr(settings, 'TWILIO_ACCOUNT_SID', '')
            auth_token = getattr(settings, 'TWILIO_AUTH_TOKEN', '')
            from_number = getattr(settings, 'TWILIO_PHONE_NUMBER', '')
            
            if not all([account_sid, auth_token, from_number]):
                logger.warning("Twilio credentials not configured")
                return
            
            client = Client(account_sid, auth_token)
            message_body = self._get_sms_message(template_name, context)
            
            message = client.messages.create(
                body=message_body,
                from_=from_number,
                to=phone_number
            )
            
            logger.info(f"SMS sent successfully to {phone_number}: {message.sid}")
            
        except Exception as e:
            logger.error(f"Failed to send SMS to {phone_number}: {e}")
    
    def send_whatsapp_notification(self, whatsapp_number, template_name, context):
        """Send WhatsApp notification via Meta Business API"""
        try:
            access_token = getattr(settings, 'WHATSAPP_ACCESS_TOKEN', '')
            phone_number_id = getattr(settings, 'WHATSAPP_PHONE_NUMBER_ID', '')
            
            if not all([access_token, phone_number_id]):
                logger.warning("WhatsApp credentials not configured")
                return
            
            url = f"https://graph.facebook.com/v18.0/{phone_number_id}/messages"
            headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
            }
            
            message_body = self._get_whatsapp_message(template_name, context)
            
            data = {
                'messaging_product': 'whatsapp',
                'to': whatsapp_number,
                'type': 'text',
                'text': {
                    'body': message_body
                }
            }
            
            response = requests.post(url, headers=headers, json=data)
            
            if response.status_code == 200:
                logger.info(f"WhatsApp message sent successfully to {whatsapp_number}")
            else:
                logger.error(f"Failed to send WhatsApp message: {response.text}")
                
        except Exception as e:
            logger.error(f"Failed to send WhatsApp message to {whatsapp_number}: {e}")
    
    def _get_default_subject(self, template_name, context):
        """Get default email subject"""
        if template_name == 'price_alert':
            return f"Price Alert: {context['product'].name}"
        elif template_name == 'deal_notification':
            return f"Deal Alert: {context['product'].name}"
        elif template_name == 'order_confirmation':
            return f"Order Confirmation: #{context.get('order_id', 'N/A')}"
        return "Express Deals Notification"
    
    def _get_default_body(self, template_name, context):
        """Get default email body"""
        if template_name == 'price_alert':
            return f"""Dear {context['user'].first_name or context['user'].username},

The price for {context['product'].name} has changed!

{context['alert_type']}: {context['price_info']}

View product: {context['site_url']}/products/{context['product'].id}/

Best regards,
Express Deals Team"""
        elif template_name == 'deal_notification':
            return f"""Dear {context['user'].first_name or context['user'].username},

We found a great deal for you!

{context['product'].name}
Price: {context['price_info']}

View deal: {context['site_url']}/products/{context['product'].id}/

Best regards,
Express Deals Team"""
        return "Express Deals Notification"
    
    def _get_sms_message(self, template_name, context):
        """Get SMS message text"""
        if template_name == 'price_alert':
            return f"Price Alert: {context['product'].name} - {context['price_info']}. View: {context['site_url']}/products/{context['product'].id}/"
        elif template_name == 'deal_notification':
            return f"Deal Alert: {context['product'].name} - {context['price_info']}. View: {context['site_url']}/products/{context['product'].id}/"
        return "Express Deals Notification"
    
    def _get_whatsapp_message(self, template_name, context):
        """Get WhatsApp message text"""
        if template_name == 'price_alert':
            return f"""🔔 *Price Alert from Express Deals*

📦 *Product:* {context['product'].name}
💰 *{context['alert_type']}:* {context['price_info']}

👀 View product: {context['site_url']}/products/{context['product'].id}/

Happy shopping! 🛒"""
        elif template_name == 'deal_notification':
            return f"""🎉 *Deal Alert from Express Deals*

📦 *Product:* {context['product'].name}
💰 *Price:* {context['price_info']}

🔥 Don't miss this deal: {context['site_url']}/products/{context['product'].id}/

Happy shopping! 🛒"""
        return "Express Deals Notification"


# Global notification service instance
notification_service = NotificationService()


# Convenience functions
def send_price_alert(user, product, alert_type, price_info):
    """Send price alert notification"""
    return notification_service.send_price_alert(user, product, alert_type, price_info)


def send_deal_notification(user, product, price_info):
    """Send deal notification"""
    context = {
        'user': user,
        'product': product,
        'price_info': price_info,
        'site_url': getattr(settings, 'SITE_URL', 'http://localhost:8000'),
    }
    
    if notification_service.email_enabled and user.email:
        notification_service.send_email_notification(user.email, 'deal_notification', context)
    
    if notification_service.sms_enabled and hasattr(user, 'profile') and user.profile.phone_number:
        notification_service.send_sms_notification(user.profile.phone_number, 'deal_notification', context)
    
    if notification_service.whatsapp_enabled and hasattr(user, 'profile') and user.profile.whatsapp_number:
        notification_service.send_whatsapp_notification(user.profile.whatsapp_number, 'deal_notification', context)


def send_order_confirmation(user, order):
    """Send order confirmation notification"""
    context = {
        'user': user,
        'order': order,
        'order_id': order.id,
        'site_url': getattr(settings, 'SITE_URL', 'http://localhost:8000'),
    }
    
    if notification_service.email_enabled and user.email:
        notification_service.send_email_notification(user.email, 'order_confirmation', context)


# Utility functions for backward compatibility
def send_notification(user, verb, **kwargs):
    """Simple notification function for backward compatibility"""
    logger.info(f"Notification: {user.username} - {verb}")
    return True


def notify_users(users, verb, **kwargs):
    """Notify multiple users"""
    for user in users:
        send_notification(user, verb, **kwargs)
    return True
