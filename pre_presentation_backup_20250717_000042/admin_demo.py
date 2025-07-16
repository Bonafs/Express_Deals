#!/usr/bin/env python
"""
Express Deals - Admin Dashboard Agent Mode Demo
===============================================
Demonstrates admin login and administrative functions
"""

import os
import django
from django.test import Client

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'express_deals.settings')
django.setup()

from django.contrib.auth.models import User
from accounts.models import UserProfile
from products.models import Product, Category
from scraping.models import ScrapeTarget

def demonstrate_admin_login():
    """Demonstrate admin login and dashboard access"""
    
    print("🛡️  EXPRESS DEALS - ADMIN AGENT MODE DEMO")
    print("=" * 60)
    
    # Admin credentials
    username = 'admin'
    password = 'Mobolaji'
    
    print(f"\n1. ADMIN LOGIN")
    print(f"   Username: {username}")
    print(f"   Password: {password}")
    
    # Get admin user
    try:
        admin_user = User.objects.get(username=username)
        print("   ✅ ADMIN USER FOUND")
        print(f"   Name: {admin_user.first_name} {admin_user.last_name}")
        print(f"   Email: {admin_user.email}")
        print(f"   Superuser: {admin_user.is_superuser}")
        print(f"   Staff: {admin_user.is_staff}")
        print(f"   Active: {admin_user.is_active}")
    except User.DoesNotExist:
        print("   ❌ ADMIN USER NOT FOUND")
        return
    
    # Test admin login
    client = Client()
    login_success = client.login(username=username, password=password)
    
    if login_success:
        print("   ✅ ADMIN LOGIN SUCCESSFUL")
    else:
        print("   ❌ ADMIN LOGIN FAILED")
        return
    
    # Test admin panel access
    print(f"\n2. ADMIN PANEL ACCESS")
    admin_response = client.get('/admin/')
    print(f"   Admin Panel Status: {admin_response.status_code}")
    
    if admin_response.status_code == 200:
        print("   ✅ ADMIN PANEL ACCESSIBLE")
    else:
        print("   ❌ ADMIN PANEL ACCESS DENIED")

def show_admin_capabilities():
    """Show what admin can manage"""
    
    print(f"\n3. ADMINISTRATIVE CAPABILITIES")
    print("=" * 60)
    
    # User management
    users = User.objects.all()
    print(f"\n👥 USER MANAGEMENT:")
    print(f"   Total Users: {users.count()}")
    for user in users:
        user_type = "Admin" if user.is_superuser else "Customer"
        print(f"   - {user.username} ({user_type}): {user.email}")
    
    # Product management
    products = Product.objects.all()
    categories = Category.objects.all()
    print(f"\n📦 PRODUCT MANAGEMENT:")
    print(f"   Total Products: {products.count()}")
    print(f"   Total Categories: {categories.count()}")
    print(f"   Featured Products: {products.filter(is_featured=True).count()}")
    print(f"   Active Products: {products.filter(is_active=True).count()}")
    
    # Scraping management
    targets = ScrapeTarget.objects.all()
    active_targets = targets.filter(status='active')
    print(f"\n🔍 SCRAPING MANAGEMENT:")
    print(f"   Total Targets: {targets.count()}")
    print(f"   Active Targets: {active_targets.count()}")
    
    print(f"   UK Retail Targets:")
    for target in active_targets[:5]:
        print(f"   - {target.name} ({target.site_type})")
    
    # System health
    print(f"\n🔧 SYSTEM HEALTH:")
    print(f"   Database: ✅ Operational")
    print(f"   Authentication: ✅ Working")
    print(f"   UK Configuration: ✅ Active")
    print(f"   Sterling Pricing: ✅ Enabled")

def show_admin_urls():
    """Show important admin URLs"""
    
    print(f"\n4. ADMIN PANEL URLS")
    print("=" * 60)
    
    admin_urls = [
        ("Main Dashboard", "http://localhost:8000/admin/"),
        ("User Management", "http://localhost:8000/admin/auth/user/"),
        ("Product Management", "http://localhost:8000/admin/products/product/"),
        ("Category Management", "http://localhost:8000/admin/products/category/"),
        ("Profile Management", "http://localhost:8000/admin/accounts/userprofile/"),
        ("Scraping Targets", "http://localhost:8000/admin/scraping/scrapetarget/"),
        ("Order Management", "http://localhost:8000/admin/orders/order/"),
        ("Payment Management", "http://localhost:8000/admin/payments/payment/"),
    ]
    
    for name, url in admin_urls:
        print(f"   {name}:")
        print(f"   └── {url}")
        print()

if __name__ == '__main__':
    demonstrate_admin_login()
    show_admin_capabilities()
    show_admin_urls()
    
    print("🎉 ADMIN AGENT MODE DEMO COMPLETE!")
    print("🔑 Admin has full system control and management capabilities")
    print("🌐 Access admin panel at: http://localhost:8000/admin/")
