#!/usr/bin/env python
"""
Authentication Test Script
==========================
Test both admin and bonafs user authentication
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'express_deals.settings')
django.setup()

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from accounts.models import UserProfile

def main():
    print("🔐 AUTHENTICATION TEST")
    print("=" * 40)
    
    # Test admin authentication
    admin = authenticate(username='admin', password='Mobolaji')
    if admin:
        print("✅ Admin login: SUCCESS")
        print(f"   Details: {admin.username} ({admin.email})")
        print(f"   Superuser: {admin.is_superuser}")
        print(f"   Staff: {admin.is_staff}")
        print(f"   Active: {admin.is_active}")
    else:
        print("❌ Admin login: FAILED")
    
    print()
    
    # Test bonafs authentication
    bonafs = authenticate(username='bonafs', password='expressdeals')
    if bonafs:
        print("✅ Bonafs login: SUCCESS")
        print(f"   Details: {bonafs.username} ({bonafs.email})")
        print(f"   Name: {bonafs.first_name} {bonafs.last_name}")
        print(f"   Active: {bonafs.is_active}")
        
        # Check profile
        try:
            profile = UserProfile.objects.get(user=bonafs)
            print(f"   Profile: EXISTS")
            print(f"   Phone: {profile.phone_number}")
            print(f"   Address: {profile.address}")
        except UserProfile.DoesNotExist:
            print("   Profile: MISSING")
    else:
        print("❌ Bonafs login: FAILED")
    
    print()
    print("=" * 40)
    
    if admin and bonafs:
        print("🎉 ALL AUTHENTICATION TESTS PASSED!")
        print("🚀 Ready for agent mode testing")
    else:
        print("❌ Some authentication tests failed")
    
    print()
    print("📋 LOGIN CREDENTIALS:")
    print("   Admin: admin / Mobolaji")
    print("   Bonafs: bonafs / expressdeals")

if __name__ == '__main__':
    main()
