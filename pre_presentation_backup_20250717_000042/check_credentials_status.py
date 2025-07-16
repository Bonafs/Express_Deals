#!/usr/bin/env python
"""
Express Deals - Live Credentials Status Check
Quick verification of SMS, WhatsApp, and Email credentials
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'express_deals.settings')
django.setup()

from django.conf import settings

def check_credentials_status():
    """Check the current status of all notification credentials"""
    print("🔐 EXPRESS DEALS - LIVE CREDENTIALS STATUS CHECK")
    print("=" * 60)
    
    # Email Configuration Check
    print("📧 EMAIL CONFIGURATION:")
    print(f"   Backend: {getattr(settings, 'EMAIL_BACKEND', 'Not configured')}")
    print(f"   Host: {getattr(settings, 'EMAIL_HOST', 'Not configured')}")
    print(f"   Port: {getattr(settings, 'EMAIL_PORT', 'Not configured')}")
    print(f"   TLS: {getattr(settings, 'EMAIL_USE_TLS', 'Not configured')}")
    print(f"   User: {getattr(settings, 'EMAIL_HOST_USER', 'Not configured')}")
    print(f"   Password: {'✅ Configured' if getattr(settings, 'EMAIL_HOST_PASSWORD', '') else '❌ Not configured'}")
    print(f"   From Email: {getattr(settings, 'DEFAULT_FROM_EMAIL', 'Not configured')}")
    print()
    
    # SMS (Twilio) Configuration Check
    print("📱 SMS (TWILIO) CONFIGURATION:")
    print(f"   Account SID: {getattr(settings, 'TWILIO_ACCOUNT_SID', 'Not configured')}")
    twilio_token = getattr(settings, 'TWILIO_AUTH_TOKEN', '')
    print(f"   Auth Token: {'✅ Configured' if twilio_token and 'your_live_twilio_auth_token_here' not in twilio_token and len(twilio_token) > 20 else '❌ Not configured (using placeholder)'}")
    print(f"   Phone Number: {getattr(settings, 'TWILIO_PHONE_NUMBER', 'Not configured')}")
    print()
    
    # WhatsApp Configuration Check
    print("💬 WHATSAPP CONFIGURATION:")
    print(f"   API URL: {getattr(settings, 'WHATSAPP_API_URL', 'Not configured')}")
    print(f"   Business API URL: {getattr(settings, 'WHATSAPP_BUSINESS_API_URL', 'Not configured')}")
    whatsapp_token = getattr(settings, 'WHATSAPP_ACCESS_TOKEN', '')
    print(f"   Access Token: {'✅ Configured' if whatsapp_token and len(whatsapp_token) > 20 else '❌ Not configured'}")
    print(f"   Phone Number ID: {getattr(settings, 'WHATSAPP_PHONE_NUMBER_ID', 'Not configured')}")
    print(f"   Verify Token: {getattr(settings, 'WHATSAPP_VERIFY_TOKEN', 'Not configured')}")
    print()
    
    # Summary
    print("=" * 60)
    print("📊 CREDENTIALS SUMMARY:")
    
    # Email status
    email_configured = (
        getattr(settings, 'EMAIL_HOST_USER', '') and 
        getattr(settings, 'EMAIL_HOST_PASSWORD', '') and
        getattr(settings, 'EMAIL_HOST', '') == 'smtp.mail.yahoo.com'
    )
    print(f"📧 Email: {'✅ LIVE CONFIGURED' if email_configured else '❌ NOT PROPERLY CONFIGURED'}")
    
    # SMS status
    sms_configured = (
        getattr(settings, 'TWILIO_ACCOUNT_SID', '') and 
        getattr(settings, 'TWILIO_AUTH_TOKEN', '') and
        'your_live_twilio_auth_token_here' not in getattr(settings, 'TWILIO_AUTH_TOKEN', '') and
        len(getattr(settings, 'TWILIO_AUTH_TOKEN', '')) > 20 and
        getattr(settings, 'TWILIO_PHONE_NUMBER', '')
    )
    print(f"📱 SMS: {'✅ LIVE CONFIGURED' if sms_configured else '❌ NEEDS LIVE TOKEN'}")
    
    # WhatsApp status
    whatsapp_configured = (
        getattr(settings, 'WHATSAPP_ACCESS_TOKEN', '') and
        len(getattr(settings, 'WHATSAPP_ACCESS_TOKEN', '')) > 20 and
        getattr(settings, 'WHATSAPP_PHONE_NUMBER_ID', '')
    )
    print(f"💬 WhatsApp: {'✅ LIVE CONFIGURED' if whatsapp_configured else '❌ NOT PROPERLY CONFIGURED'}")
    
    print("=" * 60)
    
    if email_configured and sms_configured and whatsapp_configured:
        print("🎉 ALL NOTIFICATION CHANNELS ARE LIVE AND CONFIGURED!")
    else:
        print("⚠️ SOME NOTIFICATION CHANNELS NEED CONFIGURATION")
        if not email_configured:
            print("   📧 Email needs live credentials")
        if not sms_configured:
            print("   📱 SMS needs live Twilio auth token")
        if not whatsapp_configured:
            print("   💬 WhatsApp needs live access token")

if __name__ == "__main__":
    check_credentials_status()
