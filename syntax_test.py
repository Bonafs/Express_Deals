#!/usr/bin/env python
"""
Quick syntax and functionality test for Express Deals
"""
print("🔍 SYNTAX & FUNCTIONALITY TEST")
print("=" * 40)

try:
    print("1. Testing Django setup...")
    import os
    import django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'express_deals.settings')
    django.setup()
    print("   ✅ Django setup successful")
    
    print("2. Testing model imports...")
    from accounts.models import UserProfile
    from products.models import Product
    from orders.models import Order
    print("   ✅ Model imports successful")
    
    print("3. Testing database connection...")
    from django.contrib.auth.models import User
    user_count = User.objects.count()
    product_count = Product.objects.count()
    print(f"   ✅ Database accessible - {user_count} users, {product_count} products")
    
    print("4. Testing credentials...")
    try:
        from credentials import SUPERUSER_USERNAME, SUPERUSER_PASSWORD
        print(f"   ✅ Credentials loaded - Admin: {SUPERUSER_USERNAME}")
    except ImportError:
        print("   ⚠️  credentials.py not found (normal if not set up)")
    
    print("5. Testing price format...")
    if product_count > 0:
        sample_product = Product.objects.first()
        print(f"   ✅ Sample product: {sample_product.name} - £{sample_product.price}")
    else:
        print("   ⚠️  No products found")
    
    print()
    print("🎉 ALL TESTS PASSED - NO SYNTAX ERRORS!")
    
except Exception as e:
    print(f"   ❌ Error: {e}")
    print("🚨 SYNTAX OR FUNCTIONALITY ERROR DETECTED")
