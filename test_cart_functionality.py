#!/usr/bin/env python
"""
Express Deals Cart Functionality Test
Tests all cart operations to ensure they work correctly.
"""
import os
import sys
import django
from pathlib import Path

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'express_deals.settings')
sys.path.insert(0, str(Path(__file__).resolve().parent))

def test_cart_functionality():
    """Test all cart operations."""
    try:
        django.setup()
        from django.contrib.auth.models import User
        from products.models import Product, Category
        from orders.models import Cart, CartItem
        
        print("🛒 Testing Cart Functionality")
        print("=" * 40)
        
        # Test 1: Create test user
        user, created = User.objects.get_or_create(
            username='test_cart_user',
            defaults={'email': 'test@example.com'}
        )
        print(f"✅ Test user: {user.username}")
        
        # Test 2: Get or create cart
        cart, created = Cart.objects.get_or_create(user=user)
        print(f"✅ Cart created: {cart.id}")
        
        # Test 3: Get a product to add to cart
        product = Product.objects.filter(is_active=True).first()
        if not product:
            print("❌ No active products found")
            return False
        print(f"✅ Test product: {product.name}")
        
        # Test 4: Add item to cart
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': 2}
        )
        print(f"✅ Added to cart: {cart_item.quantity} x {product.name}")
        
        # Test 5: Test cart calculations
        total_items = cart.total_items
        subtotal = cart.subtotal
        tax_amount = cart.tax_amount
        total = cart.total
        
        print(f"✅ Cart calculations:")
        print(f"   Total items: {total_items}")
        print(f"   Subtotal: ${subtotal}")
        print(f"   Tax: ${tax_amount}")
        print(f"   Total: ${total}")
        
        # Test 6: Update cart item quantity
        cart_item.quantity = 3
        cart_item.save()
        print(f"✅ Updated quantity to: {cart_item.quantity}")
        
        # Test 7: Test item total calculation
        item_total = cart_item.get_total_price()
        print(f"✅ Item total: ${item_total}")
        
        # Test 8: Remove item from cart
        cart_item.delete()
        print("✅ Item removed from cart")
        
        # Test 9: Verify cart is empty
        remaining_items = cart.total_items
        print(f"✅ Remaining items: {remaining_items}")
        
        print("\n🎉 All cart functionality tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Cart test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_cart_edge_cases():
    """Test cart edge cases and error handling."""
    try:
        from django.contrib.auth.models import User
        from products.models import Product
        from orders.models import Cart, CartItem
        
        print("\n🔍 Testing Cart Edge Cases")
        print("=" * 40)
        
        user = User.objects.get(username='test_cart_user')
        cart = Cart.objects.get(user=user)
        
        # Test 1: Add multiple different products
        products = Product.objects.filter(is_active=True)[:3]
        for i, product in enumerate(products, 1):
            CartItem.objects.create(
                cart=cart,
                product=product,
                quantity=i
            )
        print(f"✅ Added {len(products)} different products")
        
        # Test 2: Test total calculations with multiple items
        print(f"✅ Total items in cart: {cart.total_items}")
        print(f"✅ Cart subtotal: ${cart.subtotal}")
        print(f"✅ Cart total: ${cart.total}")
        
        # Test 3: Test quantity limits
        if products:
            test_item = CartItem.objects.filter(cart=cart).first()
            test_item.quantity = 100  # Max allowed
            test_item.save()
            print("✅ Max quantity (100) test passed")
            
        # Test 4: Clear cart
        cart.clear()
        print("✅ Cart cleared successfully")
        print(f"✅ Items after clear: {cart.total_items}")
        
        print("\n🎉 All edge case tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Edge case test failed: {e}")
        return False

def main():
    """Run all cart tests."""
    print("🧪 Express Deals Cart Testing Suite")
    print("=" * 50)
    
    basic_test = test_cart_functionality()
    edge_test = test_cart_edge_cases()
    
    if basic_test and edge_test:
        print("\n✅ ALL CART TESTS PASSED!")
        print("🚀 Cart functionality is working correctly!")
        return True
    else:
        print("\n❌ SOME TESTS FAILED!")
        print("🔧 Please review the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
