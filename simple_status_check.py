#!/usr/bin/env python
"""
Simple diagnostic to check current Express Deals status
"""
import os
import sys
import django

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'express_deals.settings')
django.setup()

print("🔍 EXPRESS DEALS - CURRENT STATUS CHECK")
print("=" * 50)

try:
    # Test basic Django setup
    from django.conf import settings
    print("✅ Django configuration loaded")
    
    # Test database connection
    from django.db import connection
    cursor = connection.cursor()
    cursor.execute("SELECT 1")
    print("✅ Database connection working")
    
    # Test products
    from products.models import Product
    product_count = Product.objects.count()
    print(f"✅ Products in database: {product_count}")
    
    # Test first product
    if product_count > 0:
        first_product = Product.objects.first()
        print(f"✅ First product: {first_product.name}")
        print(f"   Image field: {first_product.image}")
        if first_product.image:
            print(f"   Image URL: {first_product.image.url}")
        else:
            print("   ❌ No image set")
    
    # Test Cloudinary
    import cloudinary
    config = cloudinary.config()
    if config.cloud_name:
        print(f"✅ Cloudinary configured: {config.cloud_name}")
    else:
        print("❌ Cloudinary not configured")
    
    print("=" * 50)
    print("🎉 Basic system check completed successfully!")
    
except Exception as e:
    print(f"❌ ERROR: {e}")
    import traceback
    traceback.print_exc()
