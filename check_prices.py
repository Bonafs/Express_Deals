#!/usr/bin/env python
"""
Quick script to check current product prices
"""
import os
import sys
import django

# Setup Django environment
if __name__ == "__main__":
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'express_deals.settings')
    django.setup()
    
    from products.models import Product
    
    print("=== Current Product Prices ===")
    
    products = Product.objects.all()[:10]
    if products:
        for product in products:
            print(f"{product.name}: £{product.price}")
        
        print(f"\nTotal products: {Product.objects.count()}")
        
        # Check if any products have USD prices (unlikely but possible)
        from django.db.models import Avg
        avg_price = Product.objects.aggregate(avg_price=Avg('price'))
        print(f"Average price: £{avg_price['avg_price']:.2f}")
    else:
        print("No products found in database")
