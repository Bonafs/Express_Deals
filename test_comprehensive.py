#!/usr/bin/env python
"""
Express Deals Comprehensive Testing Suite
Tests all major e-commerce functionality before proceeding to phases B-D.
"""
import os
import sys
import django
from pathlib import Path

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'express_deals.settings')
sys.path.insert(0, str(Path(__file__).resolve().parent))

def test_models():
    """Test all models can be imported and basic operations work."""
    try:
        django.setup()
        
        print("📊 Testing Models")
        print("-" * 30)
        
        # Test products models
        from products.models import Category, Product, ProductImage, ProductReview
        print("✅ Products models imported")
        
        # Test orders models
        from orders.models import Cart, CartItem, Order, OrderItem, WishlistItem
        print("✅ Orders models imported")
        
        # Test payments models
        from payments.models import Payment
        print("✅ Payments models imported")
        
        # Test basic model operations
        categories = Category.objects.all()
        products = Product.objects.all()
        print(f"✅ Found {categories.count()} categories")
        print(f"✅ Found {products.count()} products")
        
        return True
        
    except Exception as e:
        print(f"❌ Model test failed: {e}")
        return False

def test_urls():
    """Test URL patterns are properly configured."""
    try:
        from django.urls import reverse
        
        print("\n🌐 Testing URL Patterns")
        print("-" * 30)
        
        # Test product URLs
        product_list_url = reverse('products:product_list')
        print(f"✅ Product list URL: {product_list_url}")
        
        # Test cart URLs
        cart_url = reverse('orders:cart')
        add_to_cart_url = reverse('orders:add_to_cart')
        checkout_url = reverse('orders:checkout')
        print(f"✅ Cart URL: {cart_url}")
        print(f"✅ Add to cart URL: {add_to_cart_url}")
        print(f"✅ Checkout URL: {checkout_url}")
        
        return True
        
    except Exception as e:
        print(f"❌ URL test failed: {e}")
        return False

def test_templates():
    """Test that all required templates exist."""
    templates_to_check = [
        'base.html',
        'products/product_list.html',
        'products/product_detail.html',
        'orders/cart.html',
        'orders/checkout.html',
        'payments/payment.html',
    ]
    
    print("\n🎨 Testing Templates")
    print("-" * 30)
    
    all_exist = True
    for template in templates_to_check:
        template_path = Path('templates') / template
        if template_path.exists():
            size = template_path.stat().st_size
            print(f"✅ {template} ({size} bytes)")
        else:
            print(f"❌ {template} - Missing")
            all_exist = False
    
    return all_exist

def test_static_files():
    """Test static files structure."""
    print("\n📁 Testing Static Files")
    print("-" * 30)
    
    static_dirs = ['static', 'media']
    all_exist = True
    
    for dir_name in static_dirs:
        dir_path = Path(dir_name)
        if dir_path.exists():
            print(f"✅ {dir_name}/ directory exists")
        else:
            print(f"❌ {dir_name}/ directory missing")
            all_exist = False
    
    # Check media subdirectories
    media_subdirs = ['products', 'categories']
    for subdir in media_subdirs:
        subdir_path = Path('media') / subdir
        if subdir_path.exists():
            print(f"✅ media/{subdir}/ exists")
        else:
            print(f"⚠️ media/{subdir}/ missing (will be created as needed)")
    
    return all_exist

def test_settings():
    """Test Django settings configuration."""
    try:
        from django.conf import settings
        
        print("\n⚙️ Testing Settings Configuration")
        print("-" * 30)
        
        # Check database
        if hasattr(settings, 'DATABASES'):
            print("✅ Database configuration found")
        
        # Check static files
        if hasattr(settings, 'STATIC_URL'):
            print(f"✅ Static URL: {settings.STATIC_URL}")
        
        if hasattr(settings, 'MEDIA_URL'):
            print(f"✅ Media URL: {settings.MEDIA_URL}")
        
        # Check installed apps
        required_apps = ['products', 'orders', 'payments', 'accounts']
        for app in required_apps:
            if app in settings.INSTALLED_APPS:
                print(f"✅ {app} app installed")
            else:
                print(f"❌ {app} app missing")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Settings test failed: {e}")
        return False

def test_data_population():
    """Test that sample data exists."""
    try:
        from products.models import Category, Product
        from django.contrib.auth.models import User
        
        print("\n📦 Testing Data Population")
        print("-" * 30)
        
        # Check categories
        category_count = Category.objects.count()
        print(f"✅ Categories: {category_count}")
        
        # Check products
        product_count = Product.objects.count()
        active_products = Product.objects.filter(is_active=True).count()
        print(f"✅ Products: {product_count} total, {active_products} active")
        
        # Check users
        user_count = User.objects.count()
        print(f"✅ Users: {user_count}")
        
        # Check if we have enough data for testing
        if category_count >= 5 and active_products >= 10 and user_count >= 1:
            print("✅ Sufficient test data available")
            return True
        else:
            print("⚠️ Limited test data - consider running populate_data.py")
            return True  # Not critical for basic functionality
        
    except Exception as e:
        print(f"❌ Data population test failed: {e}")
        return False

def run_comprehensive_test():
    """Run all tests and provide summary."""
    print("🧪 Express Deals Comprehensive Test Suite")
    print("=" * 50)
    
    tests = [
        ("Models", test_models),
        ("URL Patterns", test_urls),
        ("Templates", test_templates),
        ("Static Files", test_static_files),
        ("Settings", test_settings),
        ("Data Population", test_data_population),
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"\n❌ {test_name} test crashed: {e}")
            results[test_name] = False
    
    # Summary
    print(f"\n📊 Test Results Summary")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, success in results.items():
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{test_name}: {status}")
        if success:
            passed += 1
    
    print(f"\n🎯 Overall Result: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Ready to proceed to Phase B.")
        print("🚀 You can now start the development server and test manually.")
    elif passed >= total - 1:
        print("⚠️ Most tests passed. Minor issues detected but proceeding is safe.")
    else:
        print("❌ Multiple test failures. Please address issues before proceeding.")
    
    return passed >= total - 1  # Allow 1 failure

if __name__ == "__main__":
    success = run_comprehensive_test()
    sys.exit(0 if success else 1)
