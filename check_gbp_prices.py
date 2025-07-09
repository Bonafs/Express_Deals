#!/usr/bin/env python
"""
Check product prices and ensure they're in GBP
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'express_deals.settings')
django.setup()

from products.models import Product
from django.db.models import Avg, Max, Min

print('💰 CHECKING PRODUCT PRICES (GBP VERIFICATION)')
print('=' * 50)

products = Product.objects.all()
if products.exists():
    print(f'📦 Total Products: {products.count()}')
    print()
    
    for product in products[:10]:  # Show first 10 products
        print(f'• {product.name}: £{product.price}')
    
    if products.count() > 10:
        print(f'... and {products.count() - 10} more products')
    
    # Price statistics
    stats = products.aggregate(Avg('price'), Min('price'), Max('price'))
    print()
    print('📊 PRICE STATISTICS:')
    print(f'  Average: £{stats["price__avg"]:.2f}')
    print(f'  Minimum: £{stats["price__min"]:.2f}')
    print(f'  Maximum: £{stats["price__max"]:.2f}')
    
    # Check for any prices that might be in dollars (high values)
    expensive = products.filter(price__gt=1000)
    if expensive.exists():
        print()
        print('⚠️  HIGH PRICED ITEMS (Check if these should be in GBP):')
        for item in expensive:
            print(f'  • {item.name}: £{item.price}')
    else:
        print()
        print('✅ All prices appear to be in reasonable GBP ranges')
else:
    print('❌ No products found in database')
