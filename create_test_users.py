#!/usr/bin/env python
"""
Quick test superuser creation
"""
import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'express_deals.settings')
django.setup()

from django.contrib.auth.models import User

def create_test_user():
    # Create superuser
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser(
            username='admin',
            email='admin@expressdeals.co.uk',
            password='Express123!'
        )
        print("✅ Superuser 'admin' created with password 'Express123!'")
    else:
        print("📋 Superuser 'admin' already exists")
    
    # Create a test customer
    if not User.objects.filter(username='testuser').exists():
        User.objects.create_user(
            username='testuser',
            email='test@expressdeals.co.uk',
            password='Test123!',
            first_name='Test',
            last_name='Customer'
        )
        print("✅ Test user 'testuser' created with password 'Test123!'")
    else:
        print("📋 Test user 'testuser' already exists")
        
    print(f"\n🎯 Total users: {User.objects.count()}")

if __name__ == '__main__':
    create_test_user()
