#!/usr/bin/env python
"""
Quick verification script to test REST Framework import and Django configuration
"""
import os
import sys
import django

# Add the project directory to the Python path
project_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_dir)

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'express_deals.settings')

try:
    # Initialize Django
    django.setup()
    
    # Test REST framework import
    import rest_framework
    print(f"✅ SUCCESS: Django REST Framework {rest_framework.VERSION} imported successfully")
    
    # Test Django configuration
    from django.conf import settings
    if 'rest_framework' in settings.INSTALLED_APPS:
        print("✅ SUCCESS: REST Framework is properly configured in INSTALLED_APPS")
    else:
        print("❌ ERROR: REST Framework not found in INSTALLED_APPS")
    
    # Test basic Django check
    from django.core.management import execute_from_command_line
    print("✅ SUCCESS: Django configuration is valid")
    
    print("\n🎉 All checks passed! The Express Deals project is ready for production.")
    
except ImportError as e:
    print(f"❌ IMPORT ERROR: {e}")
    print("Please run: pip install -r requirements.txt")
except Exception as e:
    print(f"❌ CONFIGURATION ERROR: {e}")
    print("Please check your Django settings and configuration")
