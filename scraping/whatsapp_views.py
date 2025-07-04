"""
Express Deals - WhatsApp Webhook Handler
Handles incoming WhatsApp messages and webhook verification
"""

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.conf import settings
import json
import logging

logger = logging.getLogger(__name__)


@csrf_exempt
@require_http_methods(["GET", "POST"])
def whatsapp_webhook(request):
    """
    Handle WhatsApp webhook verification and incoming messages
    """
    if request.method == "GET":
        return verify_webhook(request)
    elif request.method == "POST":
        return handle_incoming_message(request)


def verify_webhook(request):
    """
    Verify WhatsApp webhook during setup
    """
    try:
        # Get verification parameters
        mode = request.GET.get('hub.mode')
        token = request.GET.get('hub.verify_token')
        challenge = request.GET.get('hub.challenge')
        
        # Check if mode and token are correct
        if mode == 'subscribe' and token == settings.WHATSAPP_VERIFY_TOKEN:
            logger.info("WhatsApp webhook verified successfully")
            return HttpResponse(challenge)
        else:
            logger.warning("WhatsApp webhook verification failed")
            return HttpResponse("Verification failed", status=403)
    
    except Exception as e:
        logger.error(f"WhatsApp webhook verification error: {e}")
        return HttpResponse("Verification error", status=500)


def handle_incoming_message(request):
    """
    Handle incoming WhatsApp messages
    """
    try:
        body = json.loads(request.body.decode('utf-8'))
        
        # Check if this is a WhatsApp message
        if 'entry' in body:
            for entry in body['entry']:
                if 'changes' in entry:
                    for change in entry['changes']:
                        if change.get('field') == 'messages':
                            process_whatsapp_message(change['value'])
        
        return JsonResponse({"status": "ok"})
    
    except Exception as e:
        logger.error(f"Error handling WhatsApp message: {e}")
        return JsonResponse({"status": "error", "message": str(e)}, status=500)


def process_whatsapp_message(message_data):
    """
    Process incoming WhatsApp message
    """
    try:
        if 'messages' in message_data:
            for message in message_data['messages']:
                sender_phone = message['from']
                message_text = message.get('text', {}).get('body', '')
                
                logger.info(f"Received WhatsApp message from {sender_phone}: {message_text}")
                
                # Process different types of messages
                if message_text.lower().startswith('stop'):
                    handle_unsubscribe(sender_phone)
                elif message_text.lower().startswith('help'):
                    send_help_message(sender_phone)
                elif message_text.lower().startswith('deals'):
                    send_current_deals(sender_phone)
                else:
                    send_automated_response(sender_phone, message_text)
    
    except Exception as e:
        logger.error(f"Error processing WhatsApp message: {e}")


def handle_unsubscribe(phone_number):
    """
    Handle unsubscribe request
    """
    try:
        from django.contrib.auth.models import User
        from accounts.models import UserProfile
        
        # Find user by WhatsApp number and disable notifications
        try:
            profile = UserProfile.objects.get(whatsapp_number=phone_number)
            profile.whatsapp_notifications_enabled = False
            profile.save()
            
            # Send confirmation
            from .notifications import NotificationService
            notification_service = NotificationService()
            notification_service.send_whatsapp_text_message(
                phone_number,
                "✅ You have been unsubscribed from WhatsApp notifications. To re-enable, visit your account settings on our website."
            )
            
        except UserProfile.DoesNotExist:
            logger.warning(f"No user profile found for WhatsApp number: {phone_number}")
    
    except Exception as e:
        logger.error(f"Error handling unsubscribe: {e}")


def send_help_message(phone_number):
    """
    Send help message with available commands
    """
    try:
        from .notifications import NotificationService
        
        help_text = """
🤖 *Express Deals WhatsApp Bot*

Available commands:
📦 *DEALS* - View current deals
🛑 *STOP* - Unsubscribe from notifications
❓ *HELP* - Show this help message

🛍️ Visit our website: {site_url}
📞 Customer service: support@expressdeals.com
        """.format(site_url=getattr(settings, 'SITE_URL', 'https://expressdeals.com'))
        
        notification_service = NotificationService()
        notification_service.send_whatsapp_text_message(phone_number, help_text.strip())
    
    except Exception as e:
        logger.error(f"Error sending help message: {e}")


def send_current_deals(phone_number):
    """
    Send current top deals
    """
    try:
        from products.models import Product
        from .notifications import NotificationService
        
        # Get top 3 deals (products with highest discount or lowest price)
        deals = Product.objects.filter(is_active=True).order_by('price')[:3]
        
        if deals:
            message = "🔥 *Top Deals Right Now:*\n\n"
            for i, product in enumerate(deals, 1):
                message += f"{i}. *{product.name}*\n"
                message += f"   💰 ${product.price}\n"
                if product.original_price and product.original_price > product.price:
                    discount = int(((product.original_price - product.price) / product.original_price) * 100)
                    message += f"   📉 {discount}% OFF\n"
                message += "\n"
            
            message += f"🛍️ Shop all deals: {getattr(settings, 'SITE_URL', 'https://expressdeals.com')}/products/"
        else:
            message = "🛍️ No special deals available right now. Check back soon!"
        
        notification_service = NotificationService()
        notification_service.send_whatsapp_text_message(phone_number, message)
    
    except Exception as e:
        logger.error(f"Error sending current deals: {e}")


def send_automated_response(phone_number, message_text):
    """
    Send automated response for unrecognized messages
    """
    try:
        from .notifications import NotificationService
        
        response = f"""
👋 Thanks for your message!

I'm an automated assistant. For help, send *HELP*

For customer service, please:
📧 Email: support@expressdeals.com
🌐 Visit: {getattr(settings, 'SITE_URL', 'https://expressdeals.com')}

Send *DEALS* to see current offers!
        """
        
        notification_service = NotificationService()
        notification_service.send_whatsapp_text_message(phone_number, response.strip())
    
    except Exception as e:
        logger.error(f"Error sending automated response: {e}")


class WhatsAppTemplateManager:
    """
    Manage WhatsApp message templates
    """
    
    @staticmethod
    def create_price_alert_template():
        """
        Create price alert template for WhatsApp Business API
        """
        template = {
            "name": "price_alert_template",
            "category": "MARKETING",
            "language": "en",
            "components": [
                {
                    "type": "BODY",
                    "text": "🔥 Price Alert! {{1}} is now only ${{2}} (was ${{3}}). Get it now before the price goes back up! 🛍️"
                },
                {
                    "type": "FOOTER",
                    "text": "Express Deals - Your Deal Discovery Platform"
                }
            ]
        }
        return template
    
    @staticmethod
    def create_deal_notification_template():
        """
        Create deal notification template
        """
        template = {
            "name": "deal_notification_template", 
            "category": "MARKETING",
            "language": "en",
            "components": [
                {
                    "type": "HEADER",
                    "format": "TEXT",
                    "text": "🔥 New Deals Alert!"
                },
                {
                    "type": "BODY",
                    "text": "We found {{1}} amazing deals for you! Check them out now and save big on your favorite products. 💰"
                },
                {
                    "type": "FOOTER",
                    "text": "Express Deals - Never Miss a Deal"
                }
            ]
        }
        return template
    
    @staticmethod
    def create_order_confirmation_template():
        """
        Create order confirmation template
        """
        template = {
            "name": "order_confirmation_template",
            "category": "TRANSACTIONAL", 
            "language": "en",
            "components": [
                {
                    "type": "HEADER",
                    "format": "TEXT",
                    "text": "✅ Order Confirmed"
                },
                {
                    "type": "BODY",
                    "text": "Your order #{{1}} for ${{2}} has been confirmed! We'll send you updates as it ships. Thank you for shopping with Express Deals! 📦"
                },
                {
                    "type": "FOOTER",
                    "text": "Express Deals - Fast & Reliable"
                }
            ]
        }
        return template
