#!/usr/bin/env python
"""
Quick diagnostic for image and static file issues
"""
import os
import sys
import django

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'express_deals.settings')
django.setup()

print("=== DIAGNOSTIC REPORT ===")

# Check environment variables
print("\n1. ENVIRONMENT VARIABLES:")
print(f"CLOUDINARY_CLOUD_NAME: {os.environ.get('CLOUDINARY_CLOUD_NAME', 'NOT SET')}")
print(f"CLOUDINARY_API_KEY: {os.environ.get('CLOUDINARY_API_KEY', 'NOT SET')}")
print(f"CLOUDINARY_API_SECRET: {'SET' if os.environ.get('CLOUDINARY_API_SECRET') else 'NOT SET'}")

# Check Django settings
print("\n2. DJANGO SETTINGS:")
from django.conf import settings
print(f"DEBUG: {settings.DEBUG}")
print(f"STATIC_URL: {settings.STATIC_URL}")
print(f"STATICFILES_STORAGE: {getattr(settings, 'STATICFILES_STORAGE', 'Not set')}")

# Check products
print("\n3. PRODUCT IMAGES:")
from products.models import Product
products = Product.objects.all()[:3]
for product in products:
    print(f"Product: {product.name}")
    print(f"  Image field: {product.image}")
    if product.image:
        print(f"  Image URL: {product.image.url}")
    else:
        print(f"  No image set")
    print()

# Check cloudinary config
print("\n4. CLOUDINARY CONFIG:")
try:
    import cloudinary
    config = cloudinary.config()
    print(f"Cloud name: {config.cloud_name}")
    print(f"API key: {config.api_key}")
    print(f"Secure: {config.secure}")
except Exception as e:
    print(f"Error: {e}")

print("\n=== END DIAGNOSTIC ===")
