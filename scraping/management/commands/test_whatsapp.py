"""
Django management command to test WhatsApp functionality
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from scraping.notifications import NotificationService


class Command(BaseCommand):
    help = 'Test WhatsApp notification functionality'
    
    def add_arguments(self, parser):
        parser.add_argument('phone_number', type=str, help='WhatsApp phone number to send test message')
        parser.add_argument('--message', type=str, default='Test message from Express Deals!', 
                          help='Custom test message')
        parser.add_argument('--type', type=str, choices=['text', 'price_alert', 'deal_alert'], 
                          default='text', help='Type of test message')
    
    def handle(self, *args, **options):
        phone_number = options['phone_number']
        message = options['message']
        message_type = options['type']
        
        notification_service = NotificationService()
        
        if not notification_service.whatsapp_enabled:
            self.stdout.write(
                self.style.ERROR('WhatsApp is not enabled. Please configure WHATSAPP_ACCESS_TOKEN in settings.')
            )
            return
        
        self.stdout.write(f'Sending WhatsApp {message_type} to {phone_number}...')
        
        try:
            if message_type == 'text':
                success = notification_service.send_whatsapp_text_message(phone_number, message)
            
            elif message_type == 'price_alert':
                # Create mock context for price alert
                context = {
                    'product': type('MockProduct', (), {'name': 'iPhone 15 Pro'})(),
                    'price_info': {
                        'new_price': '899.99',
                        'old_price': '999.99'
                    }
                }
                success = notification_service.send_whatsapp_price_alert(phone_number, context)
            
            elif message_type == 'deal_alert':
                # Create mock context for deal alert
                context = {
                    'deals': [
                        {
                            'product_name': 'iPhone 15 Pro',
                            'new_price': '899.99',
                            'old_price': '999.99',
                            'discount_percentage': 10
                        },
                        {
                            'product_name': 'MacBook Pro',
                            'new_price': '1799.99',
                            'old_price': '1999.99',
                            'discount_percentage': 10
                        }
                    ],
                    'site_url': 'https://expressdeals.com'
                }
                success = notification_service.send_whatsapp_deal_alert(phone_number, context)
            
            if success:
                self.stdout.write(
                    self.style.SUCCESS(f'WhatsApp {message_type} sent successfully!')
                )
            else:
                self.stdout.write(
                    self.style.ERROR(f'Failed to send WhatsApp {message_type}')
                )
        
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error sending WhatsApp message: {e}')
            )
