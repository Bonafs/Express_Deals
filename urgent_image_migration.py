#!/usr/bin/env python
"""
URGENT: Production Image Migration to Cloudinary
"""
import os
import django
import requests
from django.core.files.base import ContentFile

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'express_deals.settings')
django.setup()

from products.models import Product
import cloudinary
import cloudinary.uploader

def urgent_image_migration():
    """URGENT: Migrate all product images to Cloudinary"""
    print("🚨 URGENT IMAGE MIGRATION TO CLOUDINARY 🚨")
    
    # Set environment variables for this script
    os.environ['CLOUDINARY_CLOUD_NAME'] = 'dzecfjfju'
    os.environ['CLOUDINARY_API_KEY'] = '853483899852935' 
    os.environ['CLOUDINARY_API_SECRET'] = 'tFJ6Rb9xofDzV2Y1YrBZWaIZkhs'
    
    # Test Cloudinary connection
    try:
        result = cloudinary.api.ping()
        print("✅ Cloudinary connection: SUCCESS")
    except Exception as e:
        print(f"❌ Cloudinary connection FAILED: {e}")
        return
    
    # Get all products with images
    products = Product.objects.exclude(image='').exclude(image__isnull=True)
    print(f"📊 Found {products.count()} products with images")
    
    migrated = 0
    errors = 0
    
    for product in products:
        try:
            print(f"\n🔄 Processing: {product.name}")
            
            # Check if image is already a Cloudinary URL
            if 'cloudinary.com' in str(product.image):
                print("  ✅ Already using Cloudinary")
                continue
                
            # Get the image file path
            image_name = str(product.image).split('/')[-1]
            local_path = f"products/{image_name}"
            
            # Try to find image file locally
            possible_paths = [
                f"products/{image_name}",
                f"media/products/{image_name}",
                image_name
            ]
            
            image_found = False
            for path in possible_paths:
                if os.path.exists(path):
                    print(f"  📁 Found local file: {path}")
                    
                    # Upload to Cloudinary
                    with open(path, 'rb') as img_file:
                        result = cloudinary.uploader.upload(
                            img_file,
                            folder='products',
                            public_id=f"product_{product.id}_{image_name.split('.')[0]}",
                            overwrite=True,
                            resource_type='image'
                        )
                    
                    if result.get('secure_url'):
                        # Update product with Cloudinary public_id
                        product.image = result['public_id']
                        product.save()
                        migrated += 1
                        print(f"  ✅ MIGRATED: {result['secure_url']}")
                        image_found = True
                        break
                        
            if not image_found:
                print(f"  ⚠️  Image file not found locally")
                errors += 1
                
        except Exception as e:
            print(f"  ❌ ERROR: {str(e)}")
            errors += 1
    
    print(f"\n🎯 MIGRATION SUMMARY:")
    print(f"✅ Successfully migrated: {migrated}")
    print(f"❌ Errors: {errors}")
    print(f"📊 Total products: {products.count()}")

if __name__ == "__main__":
    urgent_image_migration()
