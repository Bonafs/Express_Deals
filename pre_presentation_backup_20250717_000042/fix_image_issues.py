#!/usr/bin/env python
"""
Upload default product image to Cloudinary and update database
"""
import os
import django
import requests

# Setup Django and environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'express_deals.settings')
os.environ['CLOUDINARY_CLOUD_NAME'] = 'dzecfjfju'
os.environ['CLOUDINARY_API_KEY'] = '853483899852935'
os.environ['CLOUDINARY_API_SECRET'] = 'tFJ6Rb9xofDzV2Y1YrBZWaIZkhs'
django.setup()

from products.models import Product
import cloudinary
import cloudinary.uploader

def upload_default_image():
    """Upload a default product image to Cloudinary"""
    print("🚨 UPLOADING DEFAULT IMAGE TO CLOUDINARY")
    
    # Create a default image URL (placeholder)
    default_image_url = "https://via.placeholder.com/600x400/2563eb/ffffff?text=Express+Deals+Product"
    
    try:
        # Download the default image
        response = requests.get(default_image_url)
        if response.status_code == 200:
            
            # Upload to Cloudinary with specific public_id
            result = cloudinary.uploader.upload(
                response.content,
                public_id='products/default',
                overwrite=True,
                resource_type='image'
            )
            
            print(f"✅ Default image uploaded: {result['secure_url']}")
            return result
        else:
            print("❌ Failed to download default image")
            return None
            
    except Exception as e:
        print(f"❌ Error uploading default image: {e}")
        return None

def fix_product_images():
    """Fix all products with default.jpg to use Cloudinary default"""
    print("\n🔄 FIXING PRODUCT IMAGE REFERENCES")
    
    # Update products using default.jpg
    products_with_default = Product.objects.filter(image__icontains='default.jpg')
    count = products_with_default.count()
    
    if count > 0:
        products_with_default.update(image='products/default')
        print(f"✅ Updated {count} products to use Cloudinary default")
    else:
        print("ℹ️  No products with default.jpg found")
    
    # Show first few products to verify
    products = Product.objects.all()[:3]
    for product in products:
        print(f"  {product.name}: {product.image}")
        try:
            print(f"    URL: {product.image.url}")
        except Exception as e:
            print(f"    ERROR: {e}")

if __name__ == "__main__":
    print("🚀 FIXING IMAGE ISSUES")
    print("=" * 50)
    
    # Upload default image
    upload_default_image()
    
    # Fix product references
    fix_product_images()
    
    print("\n✅ IMAGE FIX COMPLETE!")
