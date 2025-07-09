#!/usr/bin/env python
"""
EXPRESS DEALS - USER CREDENTIALS SETUP
Creates admin and test users with clear credentials for easy access
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'express_deals.settings')
django.setup()

from django.contrib.auth.models import User
from accounts.models import UserProfile

def setup_users():
    """Create admin and test users with clear credentials"""
    
    print("🔐 EXPRESS DEALS - USER SETUP")
    print("=" * 50)
    
    # Delete existing test users to start fresh
    User.objects.filter(username__in=['admin', 'testuser', 'customer']).delete()
    
    # Create Admin User
    admin = User.objects.create_superuser(
        username='admin',
        email='admin@expressdeals.co.uk',
        password='Admin123!',
        first_name='Express',
        last_name='Admin'
    )
    print("✅ ADMIN USER CREATED:")
    print(f"   Username: admin")
    print(f"   Password: Admin123!")
    print(f"   Email: admin@expressdeals.co.uk")
    print(f"   Access: Full admin rights")
    
    # Create Test Customer 1
    customer1 = User.objects.create_user(
        username='customer',
        email='customer@expressdeals.co.uk',
        password='Customer123!',
        first_name='John',
        last_name='Smith'
    )
    print("\n✅ CUSTOMER USER CREATED:")
    print(f"   Username: customer")
    print(f"   Password: Customer123!")
    print(f"   Email: customer@expressdeals.co.uk")
    print(f"   Access: Regular customer")
    
    # Create Test Customer 2
    customer2 = User.objects.create_user(
        username='testuser',
        email='test@expressdeals.co.uk',
        password='Test123!',
        first_name='Jane',
        last_name='Doe'
    )
    print("\n✅ TEST USER CREATED:")
    print(f"   Username: testuser")
    print(f"   Password: Test123!")
    print(f"   Email: test@expressdeals.co.uk")
    print(f"   Access: Regular customer")
    
    # Update profiles with UK details
    for user in [customer1, customer2]:
        profile = user.profile
        profile.address = f"123 High Street"
        profile.city = "London"
        profile.county = "Greater London"
        profile.postcode = "SW1A 1AA"
        profile.phone_number = "+44 20 7946 0958"
        profile.country = "United Kingdom"
        profile.preferred_currency = "GBP"
        profile.save()
    
    print("\n🇬🇧 UK PROFILES CONFIGURED:")
    print("   - UK addresses added")
    print("   - GBP currency set")
    print("   - London timezone")
    
    print("\n" + "=" * 50)
    print("🎯 QUICK ACCESS SUMMARY:")
    print("=" * 50)
    print("🔑 ADMIN LOGIN:")
    print("   URL: http://localhost:8000/admin/")
    print("   Username: admin")
    print("   Password: Admin123!")
    print("")
    print("👤 CUSTOMER LOGIN:")
    print("   URL: http://localhost:8000/accounts/login/")
    print("   Username: customer")
    print("   Password: Customer123!")
    print("")
    print("🧪 TEST USER LOGIN:")
    print("   URL: http://localhost:8000/accounts/login/")
    print("   Username: testuser")
    print("   Password: Test123!")
    print("")
    print("🌐 WEBSITE:")
    print("   URL: http://localhost:8000/")
    print("   Features: Browse products, add to cart, register")
    
    print("\n📊 STATISTICS:")
    print(f"   Total users: {User.objects.count()}")
    print(f"   Admin users: {User.objects.filter(is_superuser=True).count()}")
    print(f"   Customer users: {User.objects.filter(is_superuser=False).count()}")
    
    print("\n🚀 READY TO USE!")
    print("Run: python manage.py runserver")
    print("Then visit: http://localhost:8000")

if __name__ == '__main__':
    setup_users()
