#!/usr/bin/env python
"""
Express Deals - System Status Report
====================================
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'express_deals.settings')
django.setup()

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from accounts.models import UserProfile
from products.models import Product
from scraping.models import ScrapeTarget

def main():
    print("EXPRESS DEALS - SYSTEM STATUS REPORT")
    print("=" * 50)
    
    # Authentication Test
    print("\n1. AUTHENTICATION STATUS:")
    admin_auth = authenticate(username='admin', password='Mobolaji')
    bonafs_auth = authenticate(username='bonafs', password='expressdeals')
    
    print(f"   Admin Login: {'✅ PASS' if admin_auth else '❌ FAIL'}")
    print(f"   Bonafs Login: {'✅ PASS' if bonafs_auth else '❌ FAIL'}")
    
    # User Status
    print("\n2. USER STATUS:")
    users = User.objects.all()
    print(f"   Total Users: {users.count()}")
    for user in users:
        profile_exists = UserProfile.objects.filter(user=user).exists()
        print(f"   - {user.username}: Profile {'✅' if profile_exists else '❌'}")
    
    # Products Status
    print("\n3. PRODUCT STATUS:")
    products = Product.objects.all()
    print(f"   Total Products: {products.count()}")
    if products.exists():
        uk_products = products.filter(price__contains='£')
        print(f"   UK Products (£): {uk_products.count()}")
    
    # Scraping Targets
    print("\n4. SCRAPING TARGETS:")
    targets = ScrapeTarget.objects.all()
    print(f"   Total Targets: {targets.count()}")
    if targets.exists():
        active_targets = targets.filter(status='active')
        print(f"   Active Targets: {active_targets.count()}")
    
    # Overall Status
    print("\n5. OVERALL STATUS:")
    all_good = admin_auth and bonafs_auth and users.count() >= 4
    print(f"   System Ready: {'✅ YES' if all_good else '❌ NO'}")
    
    if all_good:
        print("\n🎉 SYSTEM IS READY FOR AGENT MODE!")
        print("🔐 Login Credentials:")
        print("   Admin: admin / Mobolaji")  
        print("   Customer: bonafs / expressdeals")
        print("🌐 Server: python manage.py runserver 8000")
    else:
        print("\n❌ System needs attention before agent mode")

if __name__ == '__main__':
    main()
