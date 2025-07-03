#!/usr/bin/env python
"""
Express Deals Sample Data Population Script
Creates categories, products, and sample data for testing.
"""
import os
import sys
import django
from pathlib import Path
from decimal import Decimal
from django.utils.text import slugify

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'express_deals.settings')
sys.path.insert(0, str(Path(__file__).resolve().parent))

try:
    django.setup()
    
    from products.models import Category, Product, ProductImage
    from django.contrib.auth.models import User
    from django.core.files.base import ContentFile
    import random

    def create_categories():
        """Create sample categories."""
        categories_data = [
            {
                'name': 'Electronics',
                'description': 'Latest electronics and gadgets including smartphones, laptops, and accessories.',
            },
            {
                'name': 'Clothing',
                'description': 'Fashion clothing for men, women, and children. Trendy and comfortable wear.',
            },
            {
                'name': 'Home & Garden',
                'description': 'Everything for your home and garden including furniture, decor, and tools.',
            },
            {
                'name': 'Sports & Outdoors',
                'description': 'Sports equipment, outdoor gear, and fitness accessories.',
            },
            {
                'name': 'Books',
                'description': 'Wide selection of books including fiction, non-fiction, and educational materials.',
            },
            {
                'name': 'Health & Beauty',
                'description': 'Health supplements, beauty products, and personal care items.',
            },
            {
                'name': 'Toys & Games',
                'description': 'Fun toys and games for children of all ages.',
            },
            {
                'name': 'Automotive',
                'description': 'Car accessories, parts, and automotive tools.',
            },
        ]
        
        categories = []
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={
                    'slug': slugify(cat_data['name']),
                    'description': cat_data['description'],
                }
            )
            categories.append(category)
            if created:
                print(f"✅ Created category: {category.name}")
        
        return categories

    def create_products(categories):
        """Create sample products."""
        products_data = [
            # Electronics
            {
                'name': 'iPhone 15 Pro Max',
                'category': 'Electronics',
                'description': 'Latest iPhone with advanced camera system and A17 Pro chip.',
                'price': Decimal('1199.99'),
                'original_price': Decimal('1299.99'),
                'stock_quantity': 50,
                'is_featured': True,
            },
            {
                'name': 'Samsung Galaxy S24 Ultra',
                'category': 'Electronics',
                'description': 'Premium Android smartphone with S Pen and excellent camera.',
                'price': Decimal('1099.99'),
                'stock_quantity': 30,
                'is_featured': True,
            },
            {
                'name': 'MacBook Air M3',
                'category': 'Electronics',
                'description': 'Lightweight laptop with Apple M3 chip and all-day battery life.',
                'price': Decimal('1299.99'),
                'original_price': Decimal('1399.99'),
                'stock_quantity': 25,
                'is_featured': True,
            },
            {
                'name': 'AirPods Pro 2',
                'category': 'Electronics',
                'description': 'Wireless earbuds with active noise cancellation.',
                'price': Decimal('249.99'),
                'stock_quantity': 100,
            },
            {
                'name': 'PlayStation 5',
                'category': 'Electronics',
                'description': 'Next-generation gaming console with 4K gaming.',
                'price': Decimal('499.99'),
                'stock_quantity': 15,
                'is_featured': True,
            },
            
            # Clothing
            {
                'name': 'Nike Air Max 270',
                'category': 'Clothing',
                'description': 'Comfortable running shoes with Max Air cushioning.',
                'price': Decimal('149.99'),
                'original_price': Decimal('169.99'),
                'stock_quantity': 75,
            },
            {
                'name': 'Levi\'s 501 Original Jeans',
                'category': 'Clothing',
                'description': 'Classic straight-leg jeans in authentic stonewash.',
                'price': Decimal('89.99'),
                'stock_quantity': 60,
            },
            {
                'name': 'Adidas Ultraboost 22',
                'category': 'Clothing',
                'description': 'High-performance running shoes with Boost technology.',
                'price': Decimal('179.99'),
                'stock_quantity': 40,
                'is_featured': True,
            },
            
            # Home & Garden
            {
                'name': 'KitchenAid Stand Mixer',
                'category': 'Home & Garden',
                'description': 'Professional-grade stand mixer for all your baking needs.',
                'price': Decimal('379.99'),
                'original_price': Decimal('429.99'),
                'stock_quantity': 20,
                'is_featured': True,
            },
            {
                'name': 'Dyson V15 Detect',
                'category': 'Home & Garden',
                'description': 'Cordless vacuum with laser dust detection.',
                'price': Decimal('649.99'),
                'stock_quantity': 35,
            },
            
            # Sports & Outdoors
            {
                'name': 'Yeti Rambler Tumbler',
                'category': 'Sports & Outdoors',
                'description': 'Insulated stainless steel tumbler keeps drinks hot or cold.',
                'price': Decimal('34.99'),
                'stock_quantity': 150,
            },
            {
                'name': 'Patagonia Down Jacket',
                'category': 'Sports & Outdoors',
                'description': 'Lightweight down jacket perfect for outdoor adventures.',
                'price': Decimal('229.99'),
                'original_price': Decimal('279.99'),
                'stock_quantity': 45,
            },
            
            # Books
            {
                'name': 'The Psychology of Programming',
                'category': 'Books',
                'description': 'Classic book on software development and programming psychology.',
                'price': Decimal('29.99'),
                'stock_quantity': 80,
            },
            {
                'name': 'Clean Code',
                'category': 'Books',
                'description': 'A handbook of agile software craftsmanship.',
                'price': Decimal('39.99'),
                'stock_quantity': 65,
                'is_featured': True,
            },
            
            # Health & Beauty
            {
                'name': 'Vitamin D3 Supplements',
                'category': 'Health & Beauty',
                'description': 'High-quality vitamin D3 supplements for immune support.',
                'price': Decimal('19.99'),
                'stock_quantity': 200,
            },
            {
                'name': 'Skincare Routine Set',
                'category': 'Health & Beauty',
                'description': 'Complete skincare routine with cleanser, toner, and moisturizer.',
                'price': Decimal('79.99'),
                'original_price': Decimal('99.99'),
                'stock_quantity': 85,
            },
        ]
        
        # Create category lookup
        cat_lookup = {cat.name: cat for cat in categories}
        
        products = []
        for product_data in products_data:
            category = cat_lookup[product_data['category']]
            
            product, created = Product.objects.get_or_create(
                name=product_data['name'],
                defaults={
                    'slug': slugify(product_data['name']),
                    'category': category,
                    'description': product_data['description'],
                    'price': product_data['price'],
                    'original_price': product_data.get('original_price'),
                    'stock_quantity': product_data['stock_quantity'],
                    'is_featured': product_data.get('is_featured', False),
                    'is_active': True,
                }
            )
            products.append(product)
            if created:
                print(f"✅ Created product: {product.name}")
        
        return products

    def create_superuser():
        """Create superuser if it doesn't exist."""
        if not User.objects.filter(is_superuser=True).exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@expressdeals.com',
                password='admin123',
                first_name='Admin',
                last_name='User'
            )
            print("✅ Created superuser: admin/admin123")
        else:
            print("✅ Superuser already exists")

    def create_sample_users():
        """Create sample regular users."""
        sample_users = [
            {
                'username': 'customer1',
                'email': 'customer1@example.com',
                'first_name': 'John',
                'last_name': 'Doe',
                'password': 'password123'
            },
            {
                'username': 'customer2',
                'email': 'customer2@example.com',
                'first_name': 'Jane',
                'last_name': 'Smith',
                'password': 'password123'
            },
        ]
        
        for user_data in sample_users:
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults={
                    'email': user_data['email'],
                    'first_name': user_data['first_name'],
                    'last_name': user_data['last_name'],
                }
            )
            if created:
                user.set_password(user_data['password'])
                user.save()
                print(f"✅ Created user: {user.username}")

    def main():
        """Main function to populate sample data."""
        print("🌱 Populating Express Deals with Sample Data")
        print("=" * 50)
        
        # Create data
        print("\n📂 Creating Categories...")
        categories = create_categories()
        
        print(f"\n🛍️ Creating Products...")
        products = create_products(categories)
        
        print(f"\n👤 Creating Users...")
        create_superuser()
        create_sample_users()
        
        # Summary
        print(f"\n🎯 Data Population Summary")
        print("=" * 50)
        print(f"📂 Categories: {Category.objects.count()}")
        print(f"🛍️ Products: {Product.objects.count()}")
        print(f"👤 Users: {User.objects.count()}")
        print(f"🌟 Featured Products: {Product.objects.filter(is_featured=True).count()}")
        
        print(f"\n🎉 Sample data populated successfully!")
        print(f"🌐 Admin login: admin/admin123")
        print(f"👤 Customer login: customer1/password123")

    if __name__ == "__main__":
        main()

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
