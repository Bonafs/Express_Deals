#!/usr/bin/env python
"""
Express Deals UK - Complete Database Setup
Populate categories and products for UK market demonstration
"""

import os
import sys
import django
from decimal import Decimal
from datetime import datetime, timedelta

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'express_deals.heroku_settings')
django.setup()

from products.models import Product, Category
from django.contrib.auth.models import User
from django.utils import timezone


def create_uk_categories():
    """Create comprehensive UK product categories"""
    print("🏷️ Creating UK Product Categories:")
    print("=" * 50)
    
    uk_categories = [
        {
            'name': 'Electronics & Technology',
            'slug': 'electronics',
            'description': 'Latest gadgets, smartphones, laptops, and tech accessories'
        },
        {
            'name': 'Home & Garden',
            'slug': 'home-garden',
            'description': 'Furniture, home decor, garden tools, and household essentials'
        },
        {
            'name': 'Fashion & Clothing',
            'slug': 'fashion',
            'description': 'Mens, womens, and childrens clothing, shoes, and accessories'
        },
        {
            'name': 'Health & Beauty',
            'slug': 'health-beauty',
            'description': 'Skincare, makeup, vitamins, and wellness products'
        },
        {
            'name': 'Sports & Outdoors',
            'slug': 'sports',
            'description': 'Fitness equipment, outdoor gear, and sporting goods'
        },
        {
            'name': 'Toys & Games',
            'slug': 'toys',
            'description': 'Children toys, board games, and educational materials'
        },
        {
            'name': 'Books & Media',
            'slug': 'books',
            'description': 'Books, DVDs, music, and digital media'
        },
        {
            'name': 'Automotive',
            'slug': 'automotive',
            'description': 'Car accessories, parts, and automotive tools'
        },
        {
            'name': 'Kitchen & Dining',
            'slug': 'kitchen',
            'description': 'Cookware, appliances, and dining accessories'
        },
        {
            'name': 'Pet Supplies',
            'slug': 'pets',
            'description': 'Food, toys, and accessories for pets'
        }
    ]
    
    created_categories = []
    for cat_data in uk_categories:
        category, created = Category.objects.get_or_create(
            slug=cat_data['slug'],
            defaults={
                'name': cat_data['name'],
                'description': cat_data['description']
            }
        )
        
        if created:
            print(f"✅ Created: {category.name}")
        else:
            print(f"📁 Exists: {category.name}")
        
        created_categories.append(category)
    
    return created_categories


def create_sample_products():
    """Create sample UK products with realistic GBP pricing"""
    print("\n📦 Creating Sample UK Products:")
    print("=" * 50)
    
    # Get categories
    categories = {cat.slug: cat for cat in Category.objects.all()}
    
    sample_products = [
        # Electronics
        {
            'name': 'iPhone 15 Pro 128GB',
            'category': 'electronics',
            'price': Decimal('999.00'),
            'original_price': Decimal('1199.00'),
            'description': 'Latest iPhone with Pro camera system and titanium design',
            'retailer': 'Amazon UK',
            'url': 'https://amazon.co.uk/iphone-15-pro',
            'image_url': 'https://via.placeholder.com/300x300?text=iPhone+15+Pro',
            'discount_percentage': 17
        },
        {
            'name': 'Samsung 65" QLED 4K Smart TV',
            'category': 'electronics',
            'price': Decimal('699.99'),
            'original_price': Decimal('899.99'),
            'description': 'Quantum Dot technology with Alexa built-in',
            'retailer': 'Currys',
            'url': 'https://currys.co.uk/samsung-tv',
            'image_url': 'https://via.placeholder.com/300x300?text=Samsung+TV',
            'discount_percentage': 22
        },
        {
            'name': 'Apple MacBook Air M2',
            'category': 'electronics',
            'price': Decimal('849.00'),
            'original_price': Decimal('1149.00'),
            'description': '13-inch laptop with M2 chip and all-day battery',
            'retailer': 'John Lewis',
            'url': 'https://johnlewis.com/macbook-air',
            'image_url': 'https://via.placeholder.com/300x300?text=MacBook+Air',
            'discount_percentage': 26
        },
        
        # Home & Garden
        {
            'name': 'Dyson V15 Detect Cordless Vacuum',
            'category': 'home-garden',
            'price': Decimal('449.99'),
            'original_price': Decimal('599.99'),
            'description': 'Laser dust detection and powerful suction',
            'retailer': 'Argos',
            'url': 'https://argos.co.uk/dyson-v15',
            'image_url': 'https://via.placeholder.com/300x300?text=Dyson+V15',
            'discount_percentage': 25
        },
        {
            'name': 'IKEA HEMNES Bed Frame',
            'category': 'home-garden',
            'price': Decimal('149.00'),
            'original_price': Decimal('199.00'),
            'description': 'Solid wood double bed frame with headboard',
            'retailer': 'IKEA UK',
            'url': 'https://ikea.com/gb/hemnes-bed',
            'image_url': 'https://via.placeholder.com/300x300?text=HEMNES+Bed',
            'discount_percentage': 25
        },
        
        # Fashion
        {
            'name': 'Nike Air Max 90 Trainers',
            'category': 'fashion',
            'price': Decimal('79.99'),
            'original_price': Decimal('109.99'),
            'description': 'Classic Nike trainers in multiple colors',
            'retailer': 'JD Sports',
            'url': 'https://jdsports.co.uk/nike-air-max',
            'image_url': 'https://via.placeholder.com/300x300?text=Nike+Air+Max',
            'discount_percentage': 27
        },
        {
            'name': 'Zara Wool Blend Coat',
            'category': 'fashion',
            'price': Decimal('59.99'),
            'original_price': Decimal('89.99'),
            'description': 'Elegant winter coat in navy blue',
            'retailer': 'Zara UK',
            'url': 'https://zara.com/uk/wool-coat',
            'image_url': 'https://via.placeholder.com/300x300?text=Zara+Coat',
            'discount_percentage': 33
        },
        
        # Health & Beauty
        {
            'name': 'The Ordinary Skincare Set',
            'category': 'health-beauty',
            'price': Decimal('24.99'),
            'original_price': Decimal('34.99'),
            'description': 'Complete skincare routine with serums and moisturizer',
            'retailer': 'Boots',
            'url': 'https://boots.com/ordinary-set',
            'image_url': 'https://via.placeholder.com/300x300?text=Skincare+Set',
            'discount_percentage': 29
        },
        
        # Sports
        {
            'name': 'Adidas Football Boots',
            'category': 'sports',
            'price': Decimal('89.99'),
            'original_price': Decimal('129.99'),
            'description': 'Professional football boots with studs',
            'retailer': 'Sports Direct',
            'url': 'https://sportsdirect.com/adidas-boots',
            'image_url': 'https://via.placeholder.com/300x300?text=Football+Boots',
            'discount_percentage': 31
        },
        
        # Kitchen
        {
            'name': 'KitchenAid Stand Mixer',
            'category': 'kitchen',
            'price': Decimal('299.99'),
            'original_price': Decimal('399.99'),
            'description': 'Professional stand mixer in classic red',
            'retailer': 'John Lewis',
            'url': 'https://johnlewis.com/kitchenaid',
            'image_url': 'https://via.placeholder.com/300x300?text=KitchenAid',
            'discount_percentage': 25
        }
    ]
    
    created_products = []
    for product_data in sample_products:
        category = categories.get(product_data['category'])
        if not category:
            print(f"❌ Category not found: {product_data['category']}")
            continue
        
        product, created = Product.objects.get_or_create(
            name=product_data['name'],
            defaults={
                'category': category,
                'price': product_data['price'],
                'original_price': product_data['original_price'],
                'description': product_data['description'],
                'retailer': product_data['retailer'],
                'url': product_data['url'],
                'image_url': product_data['image_url'],
                'discount_percentage': product_data['discount_percentage'],
                'is_available': True,
                'last_updated': timezone.now()
            }
        )
        
        if created:
            print(f"✅ Created: {product.name} - £{product.price}")
        else:
            print(f"📁 Exists: {product.name} - £{product.price}")
            
        created_products.append(product)
    
    return created_products


def update_existing_products():
    """Update any existing products to ensure they have proper UK pricing"""
    print("\n🔄 Updating Existing Products:")
    print("=" * 50)
    
    products = Product.objects.all()
    updated_count = 0
    
    for product in products:
        # Ensure products have UK-style pricing
        if not product.original_price and product.price:
            # Add a reasonable original price for discount calculation
            product.original_price = product.price * Decimal('1.3')
            product.discount_percentage = 23
            product.save()
            updated_count += 1
            print(f"🔄 Updated: {product.name}")
    
    print(f"📊 Updated {updated_count} products with pricing")
    return updated_count


def main():
    """Main setup function"""
    print("🇬🇧 Express Deals UK - Complete Database Setup")
    print("=" * 60)
    print(f"🕐 Setup started at: {timezone.now()}")
    
    try:
        # Step 1: Create categories
        categories = create_uk_categories()
        
        # Step 2: Create sample products
        products = create_sample_products()
        
        # Step 3: Update existing products
        update_existing_products()
        
        # Summary
        print("\n🎉 Database Setup Complete!")
        print("=" * 60)
        
        total_categories = Category.objects.count()
        total_products = Product.objects.count()
        available_products = Product.objects.filter(is_available=True).count()
        
        print(f"📂 Total Categories: {total_categories}")
        print(f"📦 Total Products: {total_products}")
        print(f"✅ Available Products: {available_products}")
        
        # Show category breakdown
        print("\n📊 Products per Category:")
        for category in Category.objects.all():
            count = Product.objects.filter(category=category).count()
            print(f"   {category.name}: {count} products")
        
        print(f"\n🌐 View your site: https://express-deals.herokuapp.com/")
        print(f"⚙️ Admin panel: https://express-deals.herokuapp.com/admin/")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Setup failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == '__main__':
    main()
