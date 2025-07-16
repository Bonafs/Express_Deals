#!/usr/bin/env python
"""
Script to migrate existing product images to Cloudinary
"""

import os
import django
from django.conf import settings

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'express_deals.settings')
django.setup()

from products.models import Product
from express_deals.cloudinary_settings import upload_product_image
import cloudinary
import cloudinary.uploader

def migrate_images_to_cloudinary():
    """
    Migrate existing local product images to Cloudinary
    """
    print("=== Migrating Product Images to Cloudinary ===\n")
    
    # Get all products with images
    products_with_images = Product.objects.exclude(image='')
    print(f"Found {products_with_images.count()} products with images")
    
    migrated_count = 0
    error_count = 0
    
    for product in products_with_images:
        try:
            # Check if image file exists locally
            image_path = os.path.join(settings.BASE_DIR, 'products', product.image.name.split('/')[-1])
            
            if os.path.exists(image_path):
                print(f"Uploading: {product.name}")
                
                # Upload to Cloudinary
                with open(image_path, 'rb') as image_file:
                    result = cloudinary.uploader.upload(
                        image_file,
                        folder='products',
                        public_id=f"product_{product.id}_{product.image.name.split('/')[-1].split('.')[0]}",
                        overwrite=True
                    )
                
                # Update the product image field with Cloudinary URL
                if result.get('secure_url'):
                    # For django-cloudinary-storage, we save the public_id
                    product.image = result['public_id']
                    product.save()
                    migrated_count += 1
                    print(f"  ✓ Migrated: {result['secure_url']}")
                else:
                    print(f"  ✗ Failed to get secure URL")
                    error_count += 1
            else:
                print(f"  ⚠ Image file not found locally: {image_path}")
                error_count += 1
                
        except Exception as e:
            print(f"  ✗ Error migrating {product.name}: {str(e)}")
            error_count += 1
    
    print(f"\n=== Migration Summary ===")
    print(f"Total products: {products_with_images.count()}")
    print(f"Successfully migrated: {migrated_count}")
    print(f"Errors: {error_count}")

def test_cloudinary_urls():
    """
    Test Cloudinary URL generation
    """
    print("\n=== Testing Cloudinary URLs ===")
    
    products_with_images = Product.objects.exclude(image='')[:3]
    
    for product in products_with_images:
        try:
            print(f"\nProduct: {product.name}")
            print(f"Image field: {product.image}")
            print(f"Image URL: {product.image.url}")
            
            # Test if URL is Cloudinary
            if 'cloudinary.com' in product.image.url:
                print("  ✓ Using Cloudinary")
            else:
                print("  ⚠ Not using Cloudinary")
                
        except Exception as e:
            print(f"  ✗ Error: {str(e)}")

def main():
    """Main function"""
    print("Express Deals - Cloudinary Image Migration")
    print("==========================================\n")
    
    # Test current state
    test_cloudinary_urls()
    
    # Ask for confirmation
    response = input("\nDo you want to migrate images to Cloudinary? (y/n): ")
    if response.lower() == 'y':
        migrate_images_to_cloudinary()
        
        # Test after migration
        print("\n" + "="*50)
        test_cloudinary_urls()
    else:
        print("Migration cancelled.")

if __name__ == "__main__":
    main()
