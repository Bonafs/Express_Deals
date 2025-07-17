#!/usr/bin/env python3
import os
import sys
import django

# Add the project directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'express_deals.settings')
django.setup()

from django.contrib.auth.models import User
from orders.models import Cart, CartItem
from products.models import Product

# Get the bonafs user
try:
    bonafs_user = User.objects.get(username='bonafs')
    print(f"✅ Found user: {bonafs_user.username}")
    
    # Get or create cart for bonafs
    cart, created = Cart.objects.get_or_create(user=bonafs_user)
    if created:
        print("✅ Created new cart for bonafs")
    else:
        print("✅ Found existing cart for bonafs")
    
    # Check cart properties
    print(f"Cart ID: {cart.id}")
    print(f"Total items: {cart.total_items}")
    print(f"Subtotal: £{cart.subtotal}")
    print(f"Total: £{cart.total}")
    
    # Add a test product if cart is empty
    if cart.total_items == 0:
        # Get first product
        product = Product.objects.first()
        if product:
            CartItem.objects.create(cart=cart, product=product, quantity=1)
            print(f"✅ Added {product.name} to cart")
        else:
            print("⚠️ No products found to add to cart")
    
    print("🎯 Cart is ready for bonafs user!")
    
except User.DoesNotExist:
    print("❌ User 'bonafs' not found")
except Exception as e:
    print(f"❌ Error: {e}")
