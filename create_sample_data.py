#!/usr/bin/env python
"""
Sample data creation script for Express Deals
Run this to populate your database with sample products
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'express_deals.heroku_settings')
django.setup()

from products.models import Product, Category
from decimal import Decimal

def create_sample_data():
    """Create sample categories and products"""
    
    # Create categories
    categories = [
        {'name': 'Electronics', 'description': 'Latest gadgets and electronics'},
        {'name': 'Fashion', 'description': 'Trending fashion items'},
        {'name': 'Home & Garden', 'description': 'Home improvement and gardening'},
        {'name': 'Sports', 'description': 'Sports and fitness equipment'},
    ]
    
    created_categories = []
    for cat_data in categories:
        category, created = Category.objects.get_or_create(
            name=cat_data['name'],
            defaults={'description': cat_data['description']}
        )
        created_categories.append(category)
        if created:
            print(f"✅ Created category: {category.name}")
        else:
            print(f"📁 Category exists: {category.name}")
    
    # Create sample products
    sample_products = [
        {
            'name': 'iPhone 15 Pro',
            'description': 'Latest iPhone with advanced camera system',
            'price': Decimal('999.99'),
            'category': created_categories[0],  # Electronics
            'sku': 'IPH15PRO001',
            'stock_quantity': 50,
            'is_active': True,
        },
        {
            'name': 'Nike Air Max 270',
            'description': 'Comfortable running shoes with air cushioning',
            'price': Decimal('149.99'),
            'category': created_categories[3],  # Sports
            'sku': 'NIKE270001',
            'stock_quantity': 100,
            'is_active': True,
        },
        {
            'name': 'Samsung 4K Smart TV 55"',
            'description': 'Ultra HD Smart TV with HDR support',
            'price': Decimal('599.99'),
            'category': created_categories[0],  # Electronics
            'sku': 'SAM55TV001',
            'stock_quantity': 25,
            'is_active': True,
        },
        {
            'name': 'Designer Leather Jacket',
            'description': 'Premium leather jacket for style and comfort',
            'price': Decimal('299.99'),
            'category': created_categories[1],  # Fashion
            'sku': 'LEATHER001',
            'stock_quantity': 30,
            'is_active': True,
        },
        {
            'name': 'Robot Vacuum Cleaner',
            'description': 'Smart robot vacuum with app control',
            'price': Decimal('399.99'),
            'category': created_categories[2],  # Home & Garden
            'sku': 'ROBOT001',
            'stock_quantity': 40,
            'is_active': True,
        },
    ]
    
    for product_data in sample_products:
        product, created = Product.objects.get_or_create(
            sku=product_data['sku'],
            defaults=product_data
        )
        if created:
            print(f"✅ Created product: {product.name} - ${product.price}")
        else:
            print(f"📦 Product exists: {product.name}")
    
    print(f"\n🎉 Sample data creation complete!")
    print(f"📊 Total categories: {Category.objects.count()}")
    print(f"📦 Total products: {Product.objects.count()}")

if __name__ == '__main__':
    create_sample_data()
