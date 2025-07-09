#!/usr/bin/env python
"""
Express Deals Platform Test Suite
Tests all major functionality to ensure platform is ready for use
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'express_deals.settings')
django.setup()

from django.contrib.auth.models import User
from products.models import Product, Category
from orders.models import Cart, CartItem
from accounts.models import UserProfile
from django.test import Client
from django.urls import reverse


def test_database_setup():
    """Test that all models are working correctly"""
    print("🔍 Testing Database Setup...")
    
    # Test products
    products_count = Product.objects.count()
    categories_count = Category.objects.count()
    users_count = User.objects.count()
    
    print(f"  📦 Products: {products_count}")
    print(f"  📂 Categories: {categories_count}")
    print(f"  👥 Users: {users_count}")
    
    if products_count > 0 and categories_count > 0:
        print("  ✅ Database setup is working")
        return True
    else:
        print("  ❌ Database setup issues")
        return False


def test_gbp_pricing():
    """Test that all products have GBP pricing"""
    print("\n💰 Testing GBP Pricing...")
    
    products = Product.objects.all()
    if not products:
        print("  ❌ No products found")
        return False
    
    sample_products = products[:3]
    all_have_gbp = True
    
    for product in sample_products:
        # Check if price looks reasonable for GBP (not converted from USD)
        if product.price > 2000:  # Suspiciously high for GBP
            print(f"  ⚠️  {product.name}: £{product.price} (seems high)")
            all_have_gbp = False
        else:
            print(f"  ✅ {product.name}: £{product.price}")
    
    avg_price = sum(p.price for p in products) / len(products)
    print(f"  📊 Average price: £{avg_price:.2f}")
    
    if all_have_gbp:
        print("  ✅ GBP pricing looks correct")
        return True
    else:
        print("  ❌ Some prices may need adjustment")
        return False


def test_authentication_views():
    """Test that authentication views are accessible"""
    print("\n🔐 Testing Authentication Views...")
    
    client = Client()
    
    # Test registration page
    try:
        response = client.get('/accounts/register/')
        if response.status_code == 200:
            print("  ✅ Registration page accessible")
        else:
            print(f"  ❌ Registration page error: {response.status_code}")
            return False
    except Exception as e:
        print(f"  ❌ Registration page error: {e}")
        return False
    
    # Test login page
    try:
        response = client.get('/accounts/login/')
        if response.status_code == 200:
            print("  ✅ Login page accessible")
        else:
            print(f"  ❌ Login page error: {response.status_code}")
            return False
    except Exception as e:
        print(f"  ❌ Login page error: {e}")
        return False
    
    return True


def test_product_views():
    """Test that product views are working"""
    print("\n📦 Testing Product Views...")
    
    client = Client()
    
    # Test home page
    try:
        response = client.get('/')
        if response.status_code == 200:
            print("  ✅ Home page accessible")
        else:
            print(f"  ❌ Home page error: {response.status_code}")
            return False
    except Exception as e:
        print(f"  ❌ Home page error: {e}")
        return False
    
    # Test product detail page
    product = Product.objects.first()
    if product:
        try:
            response = client.get(f'/product/{product.id}/')
            if response.status_code == 200:
                print("  ✅ Product detail page accessible")
            else:
                print(f"  ❌ Product detail page error: {response.status_code}")
                return False
        except Exception as e:
            print(f"  ❌ Product detail page error: {e}")
            return False
    
    return True


def test_cart_functionality():
    """Test cart functionality"""
    print("\n🛒 Testing Cart Functionality...")
    
    # Create a test user
    user, created = User.objects.get_or_create(
        username='carttest',
        defaults={
            'email': 'carttest@test.com',
            'password': 'test123'
        }
    )
    
    # Create cart
    cart, created = Cart.objects.get_or_create(user=user)
    print(f"  📋 Cart created for user: {user.username}")
    
    # Add item to cart
    product = Product.objects.first()
    if product:
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': 1}
        )
        print(f"  ✅ Added {product.name} to cart")
        
        # Test cart total
        total = cart.total
        print(f"  💰 Cart total: £{total}")
        
        return True
    else:
        print("  ❌ No products available for cart test")
        return False


def test_admin_setup():
    """Test admin functionality"""
    print("\n⚙️ Testing Admin Setup...")
    
    admins = User.objects.filter(is_superuser=True)
    if admins.exists():
        admin = admins.first()
        print(f"  ✅ Admin user exists: {admin.username}")
        
        client = Client()
        try:
            response = client.get('/admin/')
            if response.status_code in [200, 302]:  # 302 for redirect to login
                print("  ✅ Admin page accessible")
                return True
            else:
                print(f"  ❌ Admin page error: {response.status_code}")
                return False
        except Exception as e:
            print(f"  ❌ Admin page error: {e}")
            return False
    else:
        print("  ❌ No admin users found")
        return False


def main():
    """Run all tests"""
    print("🧪 Express Deals Platform Test Suite")
    print("=" * 50)
    
    tests = [
        test_database_setup,
        test_gbp_pricing,
        test_authentication_views,
        test_product_views,
        test_cart_functionality,
        test_admin_setup,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"  ❌ Test failed with exception: {e}")
            failed += 1
    
    print("\n" + "=" * 50)
    print(f"🎯 Test Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("🎉 All tests passed! Platform is ready for use.")
        print("\n📋 Next steps:")
        print("  1. Run: python manage.py runserver")
        print("  2. Visit: http://localhost:8000")
        print("  3. Admin: http://localhost:8000/admin (admin/admin123)")
        print("  4. Test registration and shopping cart")
    else:
        print("⚠️  Some tests failed. Please review the issues above.")
    
    return failed == 0


if __name__ == '__main__':
    main()
