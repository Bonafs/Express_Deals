#!/usr/bin/env python
"""
Clean and create sample data for Express Deals
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'express_deals.settings')
django.setup()

from products.models import Product, Category
from decimal import Decimal
from django.utils.text import slugify

def clean_and_create_data():
    """Clean existing data and create fresh sample data"""
    
    print("🧹 Cleaning existing data...")
    Product.objects.all().delete()
    Category.objects.all().delete()
    
    print("📂 Creating categories...")
    
    # Create categories with GBP-focused descriptions
    categories_data = [
        {'name': 'Electronics', 'description': 'Latest gadgets and electronics with UK delivery'},
        {'name': 'Fashion', 'description': 'Trending UK fashion and style items'},
        {'name': 'Home & Garden', 'description': 'British home improvement and garden essentials'},
        {'name': 'Sports & Fitness', 'description': 'Sports equipment and fitness gear'},
    ]
    
    categories = []
    for cat_data in categories_data:
        category = Category.objects.create(
            name=cat_data['name'],
            slug=slugify(cat_data['name']),
            description=cat_data['description']
        )
        categories.append(category)
        print(f"✅ Created: {category.name}")
    
    print("📦 Creating products with GBP prices...")
    
    # UK-focused products with GBP pricing
    products_data = [
        {
            'name': 'iPhone 15 Pro Max',
            'description': 'Latest iPhone with professional camera system. UK warranty included.',
            'price': Decimal('899.99'),
            'original_price': Decimal('1199.99'),
            'category': categories[0],  # Electronics
            'stock_quantity': 50,
            'is_active': True,
            'is_featured': True,
        },
        {
            'name': 'Samsung Galaxy S24 Ultra',
            'description': 'Premium Android smartphone with S Pen. Fast UK delivery.',
            'price': Decimal('749.99'),
            'original_price': Decimal('1099.99'),
            'category': categories[0],  # Electronics
            'stock_quantity': 40,
            'is_active': True,
            'is_featured': True,
        },
        {
            'name': 'British Designer Wool Coat',
            'description': 'Elegant British wool coat, perfect for UK weather.',
            'price': Decimal('199.99'),
            'original_price': Decimal('349.99'),
            'category': categories[1],  # Fashion
            'stock_quantity': 25,
            'is_active': True,
        },
        {
            'name': 'Nike Air Max UK Edition',
            'description': 'Limited edition trainers with Union Jack design.',
            'price': Decimal('129.99'),
            'original_price': Decimal('169.99'),
            'category': categories[3],  # Sports
            'stock_quantity': 75,
            'is_active': True,
        },
        {
            'name': 'Dyson V15 Detect',
            'description': 'British-engineered cordless vacuum cleaner.',
            'price': Decimal('449.99'),
            'original_price': Decimal('599.99'),
            'category': categories[2],  # Home & Garden
            'stock_quantity': 30,
            'is_active': True,
            'is_featured': True,
        },
        {
            'name': 'Barbour Classic Jacket',
            'description': 'Iconic British waxed cotton jacket.',
            'price': Decimal('249.99'),
            'original_price': Decimal('395.00'),
            'category': categories[1],  # Fashion
            'stock_quantity': 35,
            'is_active': True,
        },
        {
            'name': 'Royal Doulton Tea Set',
            'description': 'Fine English bone china tea set for six.',
            'price': Decimal('79.99'),
            'original_price': Decimal('120.00'),
            'category': categories[2],  # Home & Garden
            'stock_quantity': 20,
            'is_active': True,
        },
        {
            'name': 'Sony PlayStation 5',
            'description': 'Next-gen gaming console with fast UK delivery.',
            'price': Decimal('399.99'),
            'original_price': Decimal('479.99'),
            'category': categories[0],  # Electronics
            'stock_quantity': 15,
            'is_active': True,
            'is_featured': True,
        },
    ]
    
    for product_data in products_data:
        product_data['slug'] = slugify(product_data['name'])
        
        product = Product.objects.create(**product_data)
        savings = product.original_price - product.price if product.original_price else 0
        print(f"✅ Created: {product.name} - £{product.price} (Save £{savings})")
    
    print(f"\n🎉 Sample data creation complete!")
    print(f"📊 Categories: {Category.objects.count()}")
    print(f"📦 Products: {Product.objects.count()}")
    print(f"💰 All prices are in GBP (£)")

if __name__ == '__main__':
    clean_and_create_data()
