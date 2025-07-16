#!/usr/bin/env python3
"""
EMERGENCY: Add Real Product Data for Presentation
Create actual products with real data to populate ProductListView
"""

import os
import django
from django.utils.text import slugify

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'express_deals.settings')
django.setup()

from products.models import Product, Category
from decimal import Decimal

def create_emergency_products():
    """Create real products for presentation"""
    
    print("🚨 EMERGENCY: CREATING REAL PRODUCTS FOR PRESENTATION")
    print("=" * 60)
    
    # Clear any existing products
    Product.objects.all().delete()
    print("🗑️ Cleared existing products")
    
    # Ensure categories exist
    electronics, _ = Category.objects.get_or_create(
        name='Electronics',
        defaults={'slug': 'electronics', 'description': 'Electronic devices'}
    )
    fashion, _ = Category.objects.get_or_create(
        name='Fashion',
        defaults={'slug': 'fashion', 'description': 'Clothing and accessories'}
    )
    home, _ = Category.objects.get_or_create(
        name='Home & Garden',
        defaults={'slug': 'home-garden', 'description': 'Home items'}
    )
    books, _ = Category.objects.get_or_create(
        name='Books',
        defaults={'slug': 'books', 'description': 'Books and media'}
    )
    
    # Real products with real data (based on actual UK retail)
    products_data = [
        # Electronics
        {
            'name': 'Apple iPhone 15 Pro Max 256GB',
            'description': 'Latest iPhone with titanium design, A17 Pro chip, and advanced camera system',
            'price': Decimal('1199.00'),
            'original_price': Decimal('1299.00'),
            'category': electronics,
            'stock_quantity': 15,
            'is_featured': True,
        },
        {
            'name': 'Samsung Galaxy S24 Ultra 512GB',
            'description': 'Premium Android flagship with S Pen, advanced AI features, and 200MP camera',
            'price': Decimal('1049.99'),
            'original_price': Decimal('1199.99'),
            'category': electronics,
            'stock_quantity': 8,
            'is_featured': True,
        },
        {
            'name': 'Dell XPS 13 Laptop Intel i7 16GB',
            'description': 'Ultra-portable laptop with 13.4" InfinityEdge display and premium build quality',
            'price': Decimal('899.00'),
            'original_price': Decimal('1099.00'),
            'category': electronics,
            'stock_quantity': 5,
            'is_featured': True,
        },
        {
            'name': 'Sony WH-1000XM5 Noise Cancelling Headphones',
            'description': 'Industry-leading noise cancelling with exceptional sound quality',
            'price': Decimal('279.99'),
            'original_price': Decimal('349.99'),
            'category': electronics,
            'stock_quantity': 22,
        },
        {
            'name': 'iPad Air 5th Gen 256GB WiFi',
            'description': 'Powerful and versatile iPad with M1 chip and stunning Liquid Retina display',
            'price': Decimal('679.00'),
            'category': electronics,
            'stock_quantity': 12,
        },
        
        # Fashion
        {
            'name': 'Uniqlo Men\'s Crew Neck T-Shirt',
            'description': 'Premium cotton crew neck t-shirt in multiple colors, perfect fit and comfort',
            'price': Decimal('12.90'),
            'category': fashion,
            'stock_quantity': 45,
        },
        {
            'name': 'Joules Women\'s Harbour Jersey Top',
            'description': 'Classic Breton stripe jersey top in navy and white, perfect for casual wear',
            'price': Decimal('34.95'),
            'original_price': Decimal('39.95'),
            'category': fashion,
            'stock_quantity': 18,
            'is_featured': True,
        },
        {
            'name': 'Adidas Ultraboost 22 Running Shoes',
            'description': 'Premium running shoes with BOOST midsole technology for ultimate comfort',
            'price': Decimal('159.99'),
            'original_price': Decimal('189.99'),
            'category': fashion,
            'stock_quantity': 7,
        },
        
        # Home & Garden
        {
            'name': 'IKEA MALM Bed Frame Double',
            'description': 'Stylish and affordable bed frame in white stain veneer with adjustable bed sides',
            'price': Decimal('149.00'),
            'category': home,
            'stock_quantity': 3,
            'is_featured': True,
        },
        {
            'name': 'Philips Hue Smart LED Desk Lamp',
            'description': 'Smart desk lamp with millions of colors, voice control, and app connectivity',
            'price': Decimal('89.99'),
            'original_price': Decimal('119.99'),
            'category': home,
            'stock_quantity': 11,
        },
        {
            'name': 'Emma Bridgewater Polka Dot Tea Set',
            'description': 'Beautiful hand-decorated stoneware tea set with classic polka dot design',
            'price': Decimal('125.00'),
            'category': home,
            'stock_quantity': 6,
        },
        
        # Books
        {
            'name': 'Atomic Habits by James Clear',
            'description': 'The life-changing million-copy bestseller on building good habits and breaking bad ones',
            'price': Decimal('14.99'),
            'original_price': Decimal('18.99'),
            'category': books,
            'stock_quantity': 25,
        },
        {
            'name': 'The Thursday Murder Club by Richard Osman',
            'description': 'Bestselling mystery novel featuring four unlikely detectives in a retirement village',
            'price': Decimal('8.99'),
            'original_price': Decimal('12.99'),
            'category': books,
            'stock_quantity': 14,
            'is_featured': True,
        },
        {
            'name': 'Dune by Frank Herbert',
            'description': 'Classic science fiction epic - the bestselling science fiction novel of all time',
            'price': Decimal('9.99'),
            'category': books,
            'stock_quantity': 19,
        },
        
        # Additional products to reach 15+ for pagination
        {
            'name': 'Nintendo Switch OLED Console',
            'description': 'Enhanced Nintendo Switch with vibrant OLED screen and improved audio',
            'price': Decimal('309.99'),
            'original_price': Decimal('329.99'),
            'category': electronics,
            'stock_quantity': 4,
            'is_featured': True,
        },
        {
            'name': 'Dyson V15 Detect Cordless Vacuum',
            'description': 'Powerful cordless vacuum with laser dust detection and LCD screen',
            'price': Decimal('599.99'),
            'category': home,
            'stock_quantity': 2,
            'is_featured': True,
        },
        {
            'name': 'MacBook Air M3 15-inch',
            'description': 'Apple MacBook Air with M3 chip, 15.3-inch Liquid Retina display, 8GB unified memory',
            'price': Decimal('1299.00'),
            'original_price': Decimal('1399.00'),
            'category': electronics,
            'stock_quantity': 3,
            'is_featured': True,
        },
        {
            'name': 'Lego Creator Expert Big Ben',
            'description': 'Detailed replica of London\'s iconic Big Ben clock tower with 4,163 pieces',
            'price': Decimal('249.99'),
            'category': home,
            'stock_quantity': 8,
        },
    ]
    
    # Create products
    created_count = 0
    for product_data in products_data:
        try:
            # Generate slug from name
            slug = slugify(product_data['name'])
            
            # Ensure unique slug
            original_slug = slug
            counter = 1
            while Product.objects.filter(slug=slug).exists():
                slug = f"{original_slug}-{counter}"
                counter += 1
            
            product = Product.objects.create(
                name=product_data['name'],
                slug=slug,
                description=product_data['description'],
                price=product_data['price'],
                original_price=product_data.get('original_price'),
                category=product_data['category'],
                stock_quantity=product_data.get('stock_quantity', 10),
                stock_status='in_stock',
                is_active=True,
                is_featured=product_data.get('is_featured', False),
            )
            
            created_count += 1
            status = "⭐ FEATURED" if product.is_featured else "📦"
            price_info = f"£{product.price}"
            if product.original_price and product.original_price > product.price:
                price_info += f" (was £{product.original_price})"
            print(f"{status} {product.name} - {price_info}")
            
        except Exception as e:
            print(f"❌ Error creating {product_data['name']}: {e}")
    
    # Final stats
    total_products = Product.objects.count()
    featured_products = Product.objects.filter(is_featured=True).count()
    
    print(f"\n🎯 EMERGENCY PRODUCTS CREATED!")
    print(f"   Total Products: {total_products}")
    print(f"   Featured Products: {featured_products}")
    print(f"   Categories: {Category.objects.count()}")
    
    print(f"\n📋 PRODUCTS BY CATEGORY:")
    for category in Category.objects.all():
        count = Product.objects.filter(category=category).count()
        print(f"   {category.name}: {count} products")
    
    print(f"\n💰 PRICE RANGE:")
    if total_products > 0:
        min_price = Product.objects.order_by('price').first().price
        max_price = Product.objects.order_by('-price').first().price
        print(f"   Cheapest: £{min_price}")
        print(f"   Most expensive: £{max_price}")
    
    print(f"\n✅ READY FOR PRESENTATION!")
    print(f"   ProductListView will show 12 products per page")
    print(f"   You have {total_products} products = {(total_products + 11) // 12} pages")
    print(f"   All products have: name, price, category, description, stock")
    print(f"   Featured products will appear prominently")
    
    return total_products

if __name__ == "__main__":
    create_emergency_products()
