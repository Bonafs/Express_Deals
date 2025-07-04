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
import json
from urllib.parse import urlencode

logger = logging.getLogger(__name__)


class NotificationService:
    """
    Centralized service for sending notifications via multiple channels
    """
    
    def __init__(self):
        self.email_enabled = hasattr(settings, 'EMAIL_HOST')
        self.sms_enabled = hasattr(settings, 'TWILIO_ACCOUNT_SID')
        self.whatsapp_enabled = getattr(settings, 'WHATSAPP_ENABLED', False) and hasattr(settings, 'WHATSAPP_ACCESS_TOKEN')
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
        
        # Send WhatsApp if enabled and user has WhatsApp number
        if self.whatsapp_enabled and hasattr(user, 'profile') and user.profile.whatsapp_number:
            self.send_whatsapp_notification(
                user.profile.whatsapp_number,
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
        
        # Send WhatsApp deal alert if enabled
        if self.whatsapp_enabled and hasattr(user, 'profile') and user.profile.whatsapp_number:
            self.send_whatsapp_notification(
                user.profile.whatsapp_number,
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
        
        # Send WhatsApp order confirmation if enabled
        if self.whatsapp_enabled and hasattr(order.user, 'profile') and order.user.profile.whatsapp_number:
            self.send_whatsapp_notification(
                order.user.profile.whatsapp_number,
                'order_confirmation',
                context
            )
    
    def send_whatsapp_notification(self, phone_number, template_type, context):
        """
        Send WhatsApp notification using Facebook WhatsApp Business API
        """
        try:
            # Format phone number (remove any non-digit characters)
            phone_number = ''.join(filter(str.isdigit, phone_number))
            
            # Add country code if not present (assuming US +1)
            if not phone_number.startswith('1') and len(phone_number) == 10:
                phone_number = '1' + phone_number
            
            # Choose template based on type
            if template_type == 'price_alert':
                return self.send_whatsapp_price_alert(phone_number, context)
            elif template_type == 'deal_alert':
                return self.send_whatsapp_deal_alert(phone_number, context)
            elif template_type == 'order_confirmation':
                return self.send_whatsapp_order_confirmation(phone_number, context)
            else:
                return self.send_whatsapp_text_message(phone_number, 
                    f"Express Deals notification: {template_type}")
        
        except Exception as e:
            logger.error(f"Failed to send WhatsApp notification: {e}")
            return False
    
    def send_whatsapp_price_alert(self, phone_number, context):
        """
        Send WhatsApp price alert using template message
        """
        try:
            url = f"{settings.WHATSAPP_BUSINESS_API_URL}/{settings.WHATSAPP_PHONE_NUMBER_ID}/messages"
            
            headers = {
                'Authorization': f'Bearer {settings.WHATSAPP_ACCESS_TOKEN}',
                'Content-Type': 'application/json'
            }
            
            # Price alert template message
            product = context['product']
            price_info = context['price_info']
            
            payload = {
                "messaging_product": "whatsapp",
                "to": phone_number,
                "type": "template",
                "template": {
                    "name": settings.WHATSAPP_TEMPLATES['price_alert']['name'],
                    "language": {
                        "code": settings.WHATSAPP_TEMPLATES['price_alert']['language']
                    },
                    "components": [
                        {
                            "type": "body",
                            "parameters": [
                                {
                                    "type": "text",
                                    "text": product.name
                                },
                                {
                                    "type": "text", 
                                    "text": f"${price_info['new_price']}"
                                },
                                {
                                    "type": "text",
                                    "text": f"${price_info['old_price']}"
                                }
                            ]
                        }
                    ]
                }
            }
            
            response = requests.post(url, headers=headers, json=payload)
            
            if response.status_code == 200:
                logger.info(f"WhatsApp price alert sent to {phone_number}")
                return True
            else:
                logger.error(f"WhatsApp API error: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"Failed to send WhatsApp price alert: {e}")
            return False
    
    def send_whatsapp_deal_alert(self, phone_number, context):
        """
        Send WhatsApp deal alert with multiple products
        """
        try:
            deals = context['deals']
            deal_count = len(deals)
            
            # Create a formatted message with deal information
            message = f"🔥 *Express Deals Alert!*\n\n"
            message += f"We found {deal_count} amazing deals for you:\n\n"
            
            for i, deal in enumerate(deals[:3], 1):  # Limit to 3 deals
                message += f"{i}. *{deal['product_name']}*\n"
                message += f"   💰 ${deal['new_price']} (was ${deal['old_price']})\n"
                message += f"   📉 Save {deal['discount_percentage']}%\n\n"
            
            if deal_count > 3:
                message += f"...and {deal_count - 3} more deals!\n\n"
            
            message += f"🛍️ Shop now: {context['site_url']}/deals/"
            
            return self.send_whatsapp_text_message(phone_number, message)
            
        except Exception as e:
            logger.error(f"Failed to send WhatsApp deal alert: {e}")
            return False
    
    def send_whatsapp_order_confirmation(self, phone_number, context):
        """
        Send WhatsApp order confirmation
        """
        try:
            order = context['order']
            
            message = f"✅ *Order Confirmed!*\n\n"
            message += f"Order #: {order.order_number}\n"
            message += f"Total: ${order.total_amount}\n"
            message += f"Items: {order.items.count()}\n\n"
            message += f"📦 We'll send updates as your order ships!\n\n"
            message += f"Track your order: {context['site_url']}/orders/{order.id}/"
            
            return self.send_whatsapp_text_message(phone_number, message)
            
        except Exception as e:
            logger.error(f"Failed to send WhatsApp order confirmation: {e}")
            return False
    
    def send_whatsapp_text_message(self, phone_number, message):
        """
        Send simple WhatsApp text message
        """
        try:
            url = f"{settings.WHATSAPP_BUSINESS_API_URL}/{settings.WHATSAPP_PHONE_NUMBER_ID}/messages"
            
            headers = {
                'Authorization': f'Bearer {settings.WHATSAPP_ACCESS_TOKEN}',
                'Content-Type': 'application/json'
            }
            
            payload = {
                "messaging_product": "whatsapp",
                "to": phone_number,
                "type": "text",
                "text": {
                    "body": message
                }
            }
            
            response = requests.post(url, headers=headers, json=payload)
            
            if response.status_code == 200:
                logger.info(f"WhatsApp text message sent to {phone_number}")
                return True
            else:
                logger.error(f"WhatsApp API error: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"Failed to send WhatsApp text message: {e}")
            return False
    
    def send_whatsapp_media_message(self, phone_number, media_url, caption=""):
        """
        Send WhatsApp message with media (image, video, document)
        """
        try:
            url = f"{settings.WHATSAPP_BUSINESS_API_URL}/{settings.WHATSAPP_PHONE_NUMBER_ID}/messages"
            
            headers = {
                'Authorization': f'Bearer {settings.WHATSAPP_ACCESS_TOKEN}',
                'Content-Type': 'application/json'
            }
            
            # Determine media type from URL
            media_type = "image"  # Default to image
            if media_url.lower().endswith(('.mp4', '.mov', '.avi')):
                media_type = "video"
            elif media_url.lower().endswith(('.pdf', '.doc', '.docx')):
                media_type = "document"
            
            payload = {
                "messaging_product": "whatsapp",
                "to": phone_number,
                "type": media_type,
                media_type: {
                    "link": media_url
                }
            }
            
            if caption:
                payload[media_type]["caption"] = caption
            
            response = requests.post(url, headers=headers, json=payload)
            
            if response.status_code == 200:
                logger.info(f"WhatsApp media message sent to {phone_number}")
                return True
            else:
                logger.error(f"WhatsApp API error: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"Failed to send WhatsApp media message: {e}")
            return False
