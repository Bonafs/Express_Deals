#!/usr/bin/env python
"""
Test script to verify notification module is working correctly
"""

import os
import sys
import django
from pathlib import Path

# Set up Django environment
sys.path.insert(0, str(Path(__file__).resolve().parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'express_deals.settings')

def test_notification_module():
    """Test notification module functionality"""
    print("🧪 TESTING NOTIFICATION MODULE")
    print("=" * 40)
    
    try:
        # Test 1: Import notifications
        print("\n1️⃣ Testing django-notifications-hq import...")
        import notifications
        print(f"✅ notifications imported successfully (version: {notifications.__version__})")
        
        # Test 2: Django setup
        print("\n2️⃣ Testing Django setup...")
        django.setup()
        print("✅ Django setup successful")
        
        # Test 3: Settings check
        print("\n3️⃣ Checking Django settings...")
        from django.conf import settings
        if 'notifications' in settings.INSTALLED_APPS:
            print("✅ 'notifications' found in INSTALLED_APPS")
        else:
            print("❌ 'notifications' not found in INSTALLED_APPS")
            return False
        
        # Test 4: NotificationService import
        print("\n4️⃣ Testing NotificationService import...")
        from scraping.notifications import NotificationService
        print("✅ NotificationService imported successfully")
        
        # Test 5: NotificationService initialization
        print("\n5️⃣ Testing NotificationService initialization...")
        service = NotificationService()
        print("✅ NotificationService initialized successfully")
        
        # Test 6: Check service capabilities
        print("\n6️⃣ Checking notification capabilities...")
        print(f"   📧 Email enabled: {service.email_enabled}")
        print(f"   📱 SMS enabled: {service.sms_enabled}")
        print(f"   💬 WhatsApp enabled: {service.whatsapp_enabled}")
        
        # Test 7: Database tables
        print("\n7️⃣ Checking database tables...")
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE '%notification%';")
        tables = cursor.fetchall()
        
        if tables:
            print(f"✅ Found notification tables: {[table[0] for table in tables]}")
        else:
            print("⚠️  No notification tables found - run 'python manage.py migrate'")
        
        print("\n🎉 ALL TESTS PASSED!")
        print("✅ Notification module is working correctly")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("\n🔧 SOLUTION:")
        print("1. Run: pip install django-notifications-hq==1.8.3")
        print("2. Ensure 'notifications' is in INSTALLED_APPS")
        return False
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_notification_module()
    sys.exit(0 if success else 1)
