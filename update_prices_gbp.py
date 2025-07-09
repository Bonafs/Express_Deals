#!/usr/bin/env python
"""
Express Deals - Update Prices to GBP (£)
Convert any dollar prices to British Pounds
"""

import os
import sys
import django
from decimal import Decimal

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'express_deals.heroku_settings')
django.setup()

from products.models import Product, Category


def update_prices_to_gbp():
    """Update all product prices to GBP format"""
    print("💷 Updating Product Prices to GBP (£)")
    print("=" * 50)
    
    products = Product.objects.all()
    updated_count = 0
    
    # USD to GBP conversion rate (approximate)
    usd_to_gbp_rate = Decimal('0.79')
    
    for product in products:
        # Check if product might have USD pricing (over £800 could be USD)
        needs_conversion = False
        
        if product.price > 800:  # Likely USD pricing
            # Convert to GBP
            old_price = product.price
            old_original = product.original_price or product.price
            
            product.price = (product.price * usd_to_gbp_rate).quantize(Decimal('0.01'))
            if product.original_price:
                product.original_price = (product.original_price * usd_to_gbp_rate).quantize(Decimal('0.01'))
            
            product.save()
            updated_count += 1
            
            print(f"🔄 {product.name}")
            print(f"   Old: ${old_price} -> New: £{product.price}")
            needs_conversion = True
        
        # Ensure all products have reasonable UK pricing
        if not needs_conversion:
            print(f"✅ {product.name} - £{product.price}")
    
    print(f"\n📊 Update Summary:")
    print(f"   🔄 Converted {updated_count} products from USD to GBP")
    print(f"   📦 Total products: {products.count()}")
    
    # Add some more UK-specific products if needed
    create_additional_uk_products()
    
    return updated_count


def create_additional_uk_products():
    """Add more UK-specific products with proper GBP pricing"""
    print("\n🇬🇧 Adding UK-Specific Products:")
    print("=" * 50)
    
    # Get categories
    categories = {cat.slug: cat for cat in Category.objects.all()}
    
    uk_products = [
        {
            'name': 'Tesco Finest Coffee Beans 1kg',
            'category': 'kitchen',
            'price': Decimal('8.99'),
            'original_price': Decimal('12.99'),
            'description': 'Premium Arabica coffee beans from sustainable sources'
        },
        {
            'name': 'M&S Wool Jumper',
            'category': 'fashion',
            'price': Decimal('35.99'),
            'original_price': Decimal('49.99'),
            'description': 'Pure wool crew neck jumper in navy'
        },
        {
            'name': 'Boots No7 Skincare Bundle',
            'category': 'health-beauty',
            'price': Decimal('29.99'),
            'original_price': Decimal('45.99'),
            'description': 'Complete anti-aging skincare routine'
        },
        {
            'name': 'Wickes Paint Set 2.5L',
            'category': 'home-garden',
            'price': Decimal('18.99'),
            'original_price': Decimal('24.99'),
            'description': 'Emulsion paint for interior walls - magnolia'
        },
        {
            'name': 'Next Kids School Shoes',
            'category': 'fashion',
            'price': Decimal('22.99'),
            'original_price': Decimal('29.99'),
            'description': 'Black leather school shoes sizes 10-6'
        }
    ]
    
    created_count = 0
    for product_data in uk_products:
        category = categories.get(product_data['category'])
        if not category:
            continue
            
        # Check if product already exists
        if Product.objects.filter(name=product_data['name']).exists():
            print(f"📁 Exists: {product_data['name']}")
            continue
        
        # Create product
        product = Product.objects.create(
            name=product_data['name'],
            category=category,
            price=product_data['price'],
            original_price=product_data['original_price'],
            description=product_data['description'],
            slug=product_data['name'].lower().replace(' ', '-').replace('&', 'and'),
            stock_quantity=25,
            stock_status='in_stock',
            is_active=True,
            is_featured=False
        )
        
        print(f"✅ Created: {product.name} - £{product.price}")
        created_count += 1
    
    print(f"\n📊 Added {created_count} new UK products")
    return created_count


if __name__ == '__main__':
    update_prices_to_gbp()
