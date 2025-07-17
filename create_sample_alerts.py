#!/usr/bin/env python
"""
Sample data creation for Price Discounts Alert System
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'express_deals.settings')
django.setup()

from django.contrib.auth.models import User
from alerts.models import DealCategory, PriceAlert
from products.models import Product

def create_sample_data():
    """Create sample data for testing the alerts system"""
    print("Creating sample data for Price Discounts Alert System...")
    
    # Create deal categories
    categories = [
        {'name': 'Electronics', 'slug': 'electronics', 'description': 'Tech gadgets and electronics'},
        {'name': 'Fashion', 'slug': 'fashion', 'description': 'Clothing and accessories'},
        {'name': 'Home & Garden', 'slug': 'home-garden', 'description': 'Home improvement and garden supplies'},
        {'name': 'Sports & Outdoors', 'slug': 'sports-outdoors', 'description': 'Sports equipment and outdoor gear'},
        {'name': 'Books & Media', 'slug': 'books-media', 'description': 'Books, movies, and music'},
    ]
    
    for cat_data in categories:
        category, created = DealCategory.objects.get_or_create(
            slug=cat_data['slug'],
            defaults={
                'name': cat_data['name'],
                'description': cat_data['description'],
                'is_active': True
            }
        )
        if created:
            print(f"✅ Created category: {category.name}")
        else:
            print(f"📋 Category exists: {category.name}")
    
    # Create sample user if doesn't exist
    try:
        user = User.objects.get(username='bonafs')
        print(f"📋 User exists: {user.username}")
    except User.DoesNotExist:
        user = User.objects.create_user(
            username='bonafs',
            email='bonafs@example.com',
            password='testpass123'
        )
        print(f"✅ Created user: {user.username}")
    
    # Create sample price alerts if products exist
    products = Product.objects.all()[:3]  # Get first 3 products
    
    if products:
        for i, product in enumerate(products):
            # Create price drop alert
            alert, created = PriceAlert.objects.get_or_create(
                user=user,
                product=product,
                alert_type='price_drop',
                defaults={
                    'target_price': product.price * 0.9,  # 10% discount target
                    'onset_price': product.price,
                    'current_price': product.price,
                    'is_active': True,
                    'email_enabled': True,
                    'sms_enabled': False,
                    'push_enabled': True,
                }
            )
            
            if created:
                print(f"✅ Created price alert for: {product.name}")
            else:
                print(f"📋 Price alert exists for: {product.name}")
    
    print("\n🎉 Sample data creation completed!")
    print("You can now test the alerts system at: http://localhost:8000/alerts/dashboard/")

if __name__ == '__main__':
    create_sample_data()
