#!/usr/bin/env python3
"""
Express Deals - Notification System Demo
Shows how to use the notification system in your application
"""

import os
import sys
import django
from pathlib import Path

# Add the current directory to Python path
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'express_deals.settings')
django.setup()

from scraping.notifications import send_price_alert, send_deal_notification


def demo_notifications():
    print("🎬 EXPRESS DEALS NOTIFICATION DEMO")
    print("=" * 40)
    
    # Create a mock user object
    class MockUser:
        def __init__(self):
            self.username = 'demo_user'
            self.first_name = 'John'
            self.email = 'john@example.com'
            
        class profile:
            phone_number = '+1234567890'
            whatsapp_number = '+1234567890'
    
    # Create a mock product object
    class MockProduct:
        def __init__(self):
            self.name = 'iPhone 15 Pro Max'
            self.id = 123
    
    user = MockUser()
    product = MockProduct()
    
    print(f"👤 Demo User: {user.first_name} ({user.email})")
    print(f"📦 Demo Product: {product.name}")
    print()
    
    # Demo 1: Price Alert
    print("📢 DEMO 1: Price Alert Notification")
    print("-" * 30)
    try:
        send_price_alert(
            user=user,
            product=product,
            alert_type="Price Drop",
            price_info="$999.99 (was $1199.99) - Save $200!"
        )
        print("✅ Price alert sent successfully!")
    except Exception as e:
        print(f"❌ Price alert failed: {e}")
    print()
    
    # Demo 2: Deal Notification
    print("🔥 DEMO 2: Deal Notification")
    print("-" * 30)
    try:
        send_deal_notification(
            user=user,
            product=product,
            price_info="Limited Time: $899.99 - 25% OFF!"
        )
        print("✅ Deal notification sent successfully!")
    except Exception as e:
        print(f"❌ Deal notification failed: {e}")
    print()
    
    print("💡 USAGE TIPS:")
    print("- Email notifications will be shown in console (development mode)")
    print("- Configure SMTP settings for real email delivery")
    print("- Set up Twilio for SMS notifications")
    print("- Configure WhatsApp Business API for WhatsApp messages")
    print()
    print("🎉 Notification system is ready to use!")


if __name__ == '__main__':
    demo_notifications()
