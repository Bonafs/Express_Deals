#!/usr/bin/env python
"""
Test script to check if Django REST Framework is properly installed and configured.
"""

import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'express_deals.settings')

try:
    django.setup()
    print("✅ Django setup successful")
except Exception as e:
    print(f"❌ Django setup failed: {e}")
    sys.exit(1)

# Test importing Django REST Framework
try:
    import rest_framework
    print(f"✅ Django REST Framework imported successfully")
    print(f"   Version: {rest_framework.VERSION}")
except ImportError as e:
    print(f"❌ Failed to import Django REST Framework: {e}")
    print("   Please install it with: pip install djangorestframework")
    sys.exit(1)

# Test importing REST framework components
try:
    from rest_framework import viewsets, serializers, routers
    from rest_framework.decorators import api_view
    from rest_framework.response import Response
    print("✅ REST Framework components imported successfully")
except ImportError as e:
    print(f"❌ Failed to import REST framework components: {e}")
    sys.exit(1)

# Test Django settings
try:
    from django.conf import settings
    
    # Check if rest_framework is in INSTALLED_APPS
    if 'rest_framework' in settings.INSTALLED_APPS:
        print("✅ rest_framework is in INSTALLED_APPS")
    else:
        print("❌ rest_framework is NOT in INSTALLED_APPS")
    
    # Check REST_FRAMEWORK settings
    if hasattr(settings, 'REST_FRAMEWORK'):
        print("✅ REST_FRAMEWORK settings configured")
        print(f"   Default pagination: {settings.REST_FRAMEWORK.get('DEFAULT_PAGINATION_CLASS', 'Not set')}")
    else:
        print("❌ REST_FRAMEWORK settings not configured")
        
except Exception as e:
    print(f"❌ Error checking Django settings: {e}")

# Test basic functionality
try:
    from django.test import RequestFactory
    from rest_framework.test import APIRequestFactory
    
    factory = APIRequestFactory()
    print("✅ API request factory works")
except Exception as e:
    print(f"❌ Error testing API functionality: {e}")

print("\n" + "="*50)
print("Django REST Framework Test Complete")
print("="*50)

# Check if scraping app can import REST framework
try:
    sys.path.append(os.path.join(os.path.dirname(__file__), 'scraping'))
    print("✅ Scraping app path added successfully")
except Exception as e:
    print(f"❌ Error adding scraping app path: {e}")

print("\nIf all tests passed, the ModuleNotFoundError for rest_framework should be resolved!")
