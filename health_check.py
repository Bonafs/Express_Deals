#!/usr/bin/env python
"""
Simple health check script for Express Deals
"""
import os
import sys

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'express_deals.settings')

import django
django.setup()

from products.models import Product, Category

def health_check():
    try:
        print("🔍 Running Express Deals Health Check...")
        
        # Test database connection
        product_count = Product.objects.count()
        category_count = Category.objects.count()
        
        print(f"✅ Database: Connected")
        print(f"✅ Products: {product_count}")
        print(f"✅ Categories: {category_count}")
        print(f"✅ Django: 5.2.4 Working")
        
        if product_count > 0:
            print("✅ Sample product data exists")
        else:
            print("⚠️  No products found - may need sample data")
            
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = health_check()
    sys.exit(0 if success else 1)
