#!/usr/bin/env python
"""
EXPRESS DEALS - COMMERCIAL COMPLETION AT PACE
Execute the commercial completion plan immediately
"""

import os
import django

print("🚀 EXPRESS DEALS - COMMERCIAL COMPLETION AT PACE")
print("=" * 60)

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'express_deals.settings')
django.setup()

print("✅ Django setup complete")

# Test database connectivity
try:
    from scraping.models import ScrapeTarget
    targets = ScrapeTarget.objects.filter(status='active')
    print(f"✅ Database connection: {targets.count()} active scraping targets")
except Exception as e:
    print(f"❌ Database issue: {e}")

# Test notification system
try:
    from scraping.notifications import NotificationService
    notification_service = NotificationService()
    print("✅ Notification service initialized")
    print(f"   Email enabled: {notification_service.email_enabled}")
    print(f"   SMS enabled: {notification_service.sms_enabled}")
    print(f"   WhatsApp enabled: {notification_service.whatsapp_enabled}")
except Exception as e:
    print(f"❌ Notification service issue: {e}")

# Test commercial services
try:
    from scraping.services.commercial_pipeline import commercial_pipeline
    print("✅ Commercial pipeline loaded")
    
    from scraping.services.transform_service import transformer
    print("✅ Transform service loaded")
    
    from scraping.services.fetch_service import fetch_service
    print("✅ Fetch service loaded")
    
    from scraping.services.extract_service import extractor
    print("✅ Extract service loaded")
    
    from scraping.services.load_service import loader
    print("✅ Load service loaded")
    
except Exception as e:
    print(f"❌ Commercial services issue: {e}")

# Check credentials status
print("\n📋 CREDENTIALS STATUS CHECK")
print("-" * 40)

from django.conf import settings

# Email status
email_configured = (
    getattr(settings, 'EMAIL_HOST_USER', '') and 
    getattr(settings, 'EMAIL_HOST_PASSWORD', '') and
    getattr(settings, 'EMAIL_HOST', '') == 'smtp.mail.yahoo.com'
)
print(f"📧 Email: {'✅ CONFIGURED' if email_configured else '⚠️ NEEDS LIVE CREDENTIALS'}")

# SMS status
sms_configured = (
    getattr(settings, 'TWILIO_ACCOUNT_SID', '') and 
    getattr(settings, 'TWILIO_AUTH_TOKEN', '') and
    'your_live_twilio_auth_token_here' not in getattr(settings, 'TWILIO_AUTH_TOKEN', '') and
    len(getattr(settings, 'TWILIO_AUTH_TOKEN', '')) > 20 and
    getattr(settings, 'TWILIO_PHONE_NUMBER', '')
)
print(f"📱 SMS: {'✅ CONFIGURED' if sms_configured else '⚠️ NEEDS LIVE TOKEN'}")

# WhatsApp status
whatsapp_configured = (
    getattr(settings, 'WHATSAPP_ACCESS_TOKEN', '') and
    len(getattr(settings, 'WHATSAPP_ACCESS_TOKEN', '')) > 20 and
    getattr(settings, 'WHATSAPP_PHONE_NUMBER_ID', '')
)
print(f"💬 WhatsApp: {'✅ CONFIGURED' if whatsapp_configured else '⚠️ NEEDS LIVE TOKEN'}")

# Stripe status
stripe_configured = (
    getattr(settings, 'STRIPE_PUBLISHABLE_KEY', '').startswith('pk_') and
    getattr(settings, 'STRIPE_SECRET_KEY', '').startswith('sk_')
)
print(f"💳 Stripe: {'✅ CONFIGURED' if stripe_configured else '⚠️ NEEDS LIVE KEYS'}")

print("\n🎯 COMMERCIAL SYSTEM STATUS:")
if email_configured and sms_configured and whatsapp_configured and stripe_configured:
    print("🎉 ALL SYSTEMS READY FOR COMMERCIAL OPERATION!")
else:
    print("⚠️ SOME CREDENTIALS NEED CONFIGURATION FOR FULL OPERATION")
    print("\n📋 NEXT STEPS:")
    if not email_configured:
        print("   1. Configure live email credentials")
    if not sms_configured:
        print("   2. Configure live Twilio SMS token")
    if not whatsapp_configured:
        print("   3. Configure live WhatsApp Business API token")
    if not stripe_configured:
        print("   4. Configure live Stripe payment keys")

print("\n🚀 EXPRESS DEALS COMMERCIAL COMPLETION: SYSTEMS CHECKED")
print("✅ Ready for credential configuration and full deployment!")
