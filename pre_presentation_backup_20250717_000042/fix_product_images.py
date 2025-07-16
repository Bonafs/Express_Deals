#!/usr/bin/env python
"""
Fix Product Images Script
Moves images from products/ to media/products/ and updates database
"""

import os
import shutil
import django
from pathlib import Path

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'express_deals.settings')
django.setup()

from products.models import Product, Category

def fix_product_images():
    """Fix product images by moving them and updating database"""
    
    # Base directories
    base_dir = Path(__file__).resolve().parent
    products_dir = base_dir / 'products'
    media_products_dir = base_dir / 'media' / 'products'
    
    # Ensure media/products directory exists
    media_products_dir.mkdir(parents=True, exist_ok=True)
    
    # Find all JPG files in products directory
    image_files = list(products_dir.glob('*.jpg'))
    
    print(f"Found {len(image_files)} images in products directory")
    
    # Move images to media/products
    moved_count = 0
    for image_file in image_files:
        dest_path = media_products_dir / image_file.name
        if not dest_path.exists():
            shutil.copy2(image_file, dest_path)
            moved_count += 1
            print(f"Moved: {image_file.name}")
        else:
            print(f"Already exists: {image_file.name}")
    
    print(f"Moved {moved_count} images to media/products/")
    
    # Create sample products if none exist
    if Product.objects.count() == 0:
        print("No products found. Creating sample products...")
        create_sample_products()
    else:
        # Update existing products with images
        print("Updating existing products with images...")
        update_product_images()

def create_sample_products():
    """Create sample products with images"""
    
    # Create Electronics category if it doesn't exist
    electronics, created = Category.objects.get_or_create(
        name="Electronics",
        defaults={
            'slug': 'electronics',
            'description': 'Electronic devices and gadgets'
        }
    )
    
    # Create Clothing category
    clothing, created = Category.objects.get_or_create(
        name="Clothing",
        defaults={
            'slug': 'clothing', 
            'description': 'Fashion and apparel'
        }
    )
    
    # Create Home & Kitchen category
    home, created = Category.objects.get_or_create(
        name="Home & Kitchen",
        defaults={
            'slug': 'home-kitchen',
            'description': 'Home and kitchen essentials'
        }
    )
    
    # Sample products data
    sample_products = [
        {
            'name': 'iPhone 15 Pro Max',
            'slug': 'iphone-15-pro-max',
            'category': electronics,
            'description': 'Latest iPhone with advanced features',
            'price': 1199.99,
            'original_price': 1299.99,
            'image': 'products/iphone_15_pro_max.jpg',
            'stock_quantity': 50,
        },
        {
            'name': 'Sony PlayStation 5',
            'slug': 'sony-playstation-5',
            'category': electronics,
            'description': 'Next-gen gaming console',
            'price': 499.99,
            'original_price': 549.99,
            'image': 'products/sony_playstation_5.jpg',
            'stock_quantity': 25,
        },
        {
            'name': 'Adidas Originals Stan Smith',
            'slug': 'adidas-originals-stan-smith',
            'category': clothing,
            'description': 'Classic white sneakers',
            'price': 89.99,
            'original_price': 99.99,
            'image': 'products/adidas_originals_stan_smith.jpg',
            'stock_quantity': 100,
        },
        {
            'name': 'Organic Cotton T-Shirt',
            'slug': 'organic-cotton-t-shirt',
            'category': clothing,
            'description': 'Comfortable organic cotton t-shirt',
            'price': 24.99,
            'original_price': 29.99,
            'image': 'products/organic_cotton_t-shirt.jpg',
            'stock_quantity': 75,
        },
        {
            'name': 'LED Desk Lamp',
            'slug': 'led-desk-lamp',
            'category': home,
            'description': 'Adjustable LED desk lamp with USB charging',
            'price': 45.99,
            'original_price': 59.99,
            'image': 'products/led_desk_lamp.jpg',
            'stock_quantity': 40,
        },
        {
            'name': 'Stainless Steel Water Bottle',
            'slug': 'stainless-steel-water-bottle',
            'category': home,
            'description': 'Insulated stainless steel water bottle',
            'price': 19.99,
            'original_price': 24.99,
            'image': 'products/stainless_steel_water_bottle.jpg',
            'stock_quantity': 80,
        }
    ]
    
    created_count = 0
    for product_data in sample_products:
        product, created = Product.objects.get_or_create(
            slug=product_data['slug'],
            defaults=product_data
        )
        if created:
            created_count += 1
            print(f"Created product: {product.name}")
    
    print(f"Created {created_count} new products")

def update_product_images():
    """Update existing products with proper image paths"""
    updated_count = 0
    
    for product in Product.objects.all():
        # Try to find a matching image
        product_name_clean = product.name.lower().replace(' ', '_').replace('-', '_')
        
        # Check for various image name patterns
        possible_names = [
            f"{product_name_clean}.jpg",
            f"{product.slug.replace('-', '_')}.jpg",
            # Add more patterns as needed
        ]
        
        media_products_dir = Path(__file__).resolve().parent / 'media' / 'products'
        
        for possible_name in possible_names:
            image_path = media_products_dir / possible_name
            if image_path.exists():
                product.image = f'products/{possible_name}'
                product.save()
                updated_count += 1
                print(f"Updated {product.name} with image: {possible_name}")
                break
    
    print(f"Updated {updated_count} products with images")

if __name__ == '__main__':
    print("🖼️ Fixing product images...")
    fix_product_images()
    print("✅ Product image fix complete!")
