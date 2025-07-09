#!/usr/bin/env python
"""
Simple Django setup test
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'express_deals.settings')

try:
    django.setup()
    from products.models import Product
    print(f"✅ Django setup successful")
    print(f"📦 Products in database: {Product.objects.count()}")
    
    from django.contrib.auth.models import User
    print(f"👥 Users in database: {User.objects.count()}")
    
    # Quick superuser creation
    if not User.objects.filter(is_superuser=True).exists():
        User.objects.create_superuser('admin', 'admin@test.com', 'admin123')
        print("✅ Admin user created: admin/admin123")
    else:
        print("📋 Admin user already exists")
        
except Exception as e:
    print(f"❌ Error: {e}")
