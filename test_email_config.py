#!/usr/bin/env python
"""
Express Deals - Email Configuration Test
Test the current email backend configuration
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'express_deals.settings')
django.setup()

from django.conf import settings

def test_email_config():
    """Test current email configuration"""
    print("📧 EXPRESS DEALS - EMAIL CONFIGURATION TEST")
    print("=" * 50)
    
    print(f"🐛 DEBUG Mode: {settings.DEBUG}")
    print(f"📧 Email Backend: {settings.EMAIL_BACKEND}")
    print(f"🏠 Email Host: {settings.EMAIL_HOST}")
    print(f"🔌 Email Port: {settings.EMAIL_PORT}")
    print(f"🔐 Email TLS: {settings.EMAIL_USE_TLS}")
    print(f"👤 Email User: {settings.EMAIL_HOST_USER}")
    print(f"🔑 Email Password: {'✅ Set' if settings.EMAIL_HOST_PASSWORD else '❌ Not set'}")
    print(f"📬 Default From: {settings.DEFAULT_FROM_EMAIL}")
    
    print("\n" + "=" * 50)
    
    # Check if configuration is appropriate for current mode
    if settings.DEBUG:
        if 'console' in settings.EMAIL_BACKEND:
            print("✅ DEVELOPMENT: Console backend active (emails will print to console)")
        else:
            print("⚠️ DEVELOPMENT: SMTP backend active (emails will be sent)")
    else:
        if 'smtp' in settings.EMAIL_BACKEND:
            print("✅ PRODUCTION: SMTP backend active (emails will be sent)")
            if settings.EMAIL_HOST_USER and settings.EMAIL_HOST_PASSWORD:
                print("✅ PRODUCTION: Email credentials configured")
            else:
                print("❌ PRODUCTION: Email credentials missing!")
        else:
            print("❌ PRODUCTION: Console backend active (emails won't be sent)")

if __name__ == "__main__":
    test_email_config()
