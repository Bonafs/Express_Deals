#!/usr/bin/env python
"""
Express Deals - Customer Dashboard Agent Mode Demo
==================================================
Demonstrates logging in as bonafs customer and accessing dashboard
"""

import os
import django
from django.test import Client
from django.urls import reverse

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'express_deals.settings')
django.setup()

from django.contrib.auth.models import User
from accounts.models import UserProfile
from products.models import Product, Category

def demonstrate_customer_login():
    """Demonstrate customer login and dashboard access"""
    
    print("🔐 EXPRESS DEALS - CUSTOMER AGENT MODE DEMO")
    print("=" * 60)
    
    # Create test client
    client = Client()
    
    # Bonafs customer credentials
    username = 'bonafs'
    password = 'expressdeals'
    
    print(f"\n1. LOGGING IN AS CUSTOMER")
    print(f"   Username: {username}")
    print(f"   Password: {password}")
    
    # Attempt login
    login_response = client.post('/accounts/login/', {
        'username': username,
        'password': password,
        'remember_me': False
    })
    
    if login_response.status_code == 302:  # Redirect indicates successful login
        print("   ✅ LOGIN SUCCESSFUL!")
        print(f"   Redirected to: {login_response.url}")
    else:
        print("   ❌ LOGIN FAILED!")
        print(f"   Status Code: {login_response.status_code}")
        return
    
    # Get user information
    user = User.objects.get(username=username)
    print(f"\n2. CUSTOMER PROFILE")
    print(f"   Name: {user.first_name} {user.last_name}")
    print(f"   Email: {user.email}")
    
    try:
        profile = UserProfile.objects.get(user=user)
        print(f"   Phone: {profile.phone_number}")
        print(f"   Address: {profile.address}")
        print(f"   Date of Birth: {profile.date_of_birth}")
    except UserProfile.DoesNotExist:
        print("   Profile: Not found")
    
    # Test home page access
    print(f"\n3. ACCESSING CUSTOMER DASHBOARD")
    home_response = client.get('/')
    print(f"   Home Page Status: {home_response.status_code}")
    
    if home_response.status_code == 200:
        print("   ✅ DASHBOARD ACCESSIBLE")
        
        # Get available products
        products = Product.objects.filter(is_active=True)[:5]
        print(f"\n4. AVAILABLE PRODUCTS")
        print(f"   Total Products: {Product.objects.count()}")
        print(f"   Active Products: {products.count()}")
        
        for product in products:
            print(f"   - {product.name}: {product.price}")
    
    # Test profile page access
    print(f"\n5. PROFILE PAGE ACCESS")
    try:
        profile_response = client.get('/accounts/profile/')
        print(f"   Profile Page Status: {profile_response.status_code}")
        if profile_response.status_code == 200:
            print("   ✅ PROFILE PAGE ACCESSIBLE")
        elif profile_response.status_code == 404:
            print("   ℹ️  Profile page not implemented yet")
    except:
        print("   ℹ️  Profile page endpoint not found")
    
    # Test product browsing
    print(f"\n6. PRODUCT BROWSING")
    products_response = client.get('/products/')
    if products_response.status_code == 200:
        print("   ✅ PRODUCT CATALOG ACCESSIBLE")
    else:
        print(f"   Product catalog status: {products_response.status_code}")
    
    print(f"\n🎉 CUSTOMER AGENT MODE DEMO COMPLETE!")
    print(f"📊 Customer '{username}' successfully logged in and accessed dashboard")

def show_dashboard_info():
    """Show what's available in the customer dashboard"""
    
    print(f"\n" + "=" * 60)
    print("📋 CUSTOMER DASHBOARD FEATURES")
    print("=" * 60)
    
    # Available categories
    categories = Category.objects.all()
    print(f"\n🏷️  PRODUCT CATEGORIES ({categories.count()}):")
    for category in categories:
        product_count = Product.objects.filter(category=category, is_active=True).count()
        print(f"   - {category.name}: {product_count} products")
    
    # Featured products
    featured_products = Product.objects.filter(is_featured=True, is_active=True)
    print(f"\n⭐ FEATURED PRODUCTS ({featured_products.count()}):")
    for product in featured_products[:3]:
        print(f"   - {product.name}")
        print(f"     Price: {product.price}")
        print(f"     Description: {product.description[:50]}...")
        print()
    
    # UK-specific information
    print(f"\n🇬🇧 UK MARKET FOCUS:")
    print(f"   - All prices in British Pounds (£)")
    print(f"   - UK delivery addresses supported")
    print(f"   - Major UK retailers integrated")
    print(f"   - Customer location: Bromley, Kent")

if __name__ == '__main__':
    demonstrate_customer_login()
    show_dashboard_info()
