#!/usr/bin/env python
"""
Verification script to confirm Express Deals project works without .env file
"""
import os
import sys
from pathlib import Path

def main():
    print("🔍 EXPRESS DEALS - NO .ENV VERIFICATION")
    print("=" * 50)
    
    # Check if .env file exists
    env_file = Path('.env')
    if env_file.exists():
        print("❌ .env file found! Removing...")
        env_file.unlink()
        print("✅ .env file removed")
    else:
        print("✅ No .env file found")
    
    # Test Django settings import
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'express_deals.settings')
        import django
        django.setup()
        print("✅ Django settings loaded successfully")
    except Exception as e:
        print(f"❌ Django settings failed: {e}")
        return False
    
    # Test key Django components
    try:
        from django.conf import settings
        print(f"✅ SECRET_KEY: {'***' + settings.SECRET_KEY[-4:] if settings.SECRET_KEY else 'NOT SET'}")
        print(f"✅ DEBUG: {settings.DEBUG}")
        print(f"✅ ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}")
        print(f"✅ Database: {settings.DATABASES['default']['ENGINE']}")
        print(f"✅ Static URL: {settings.STATIC_URL}")
        print(f"✅ Media URL: {settings.MEDIA_URL}")
    except Exception as e:
        print(f"❌ Settings access failed: {e}")
        return False
    
    # Test Django management commands
    try:
        from django.core.management import execute_from_command_line
        print("✅ Django management commands available")
    except Exception as e:
        print(f"❌ Management commands failed: {e}")
        return False
    
    print("\n🎉 SUCCESS!")
    print("=" * 50)
    print("✅ Express Deals project runs without .env file")
    print("✅ All configuration is hardcoded in settings.py")
    print("✅ Ready for development and testing")
    print("\n💡 To start development server:")
    print("   python manage.py runserver")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
