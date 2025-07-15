#!/usr/bin/env python
"""
URGENT: Upload sample images to Cloudinary for all products
"""
import os
import django
import requests

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'express_deals.settings')
django.setup()

from products.models import Product
import cloudinary
import cloudinary.uploader

def upload_sample_images():
    """Upload sample product images to Cloudinary"""
    print("🚨 UPLOADING SAMPLE IMAGES TO CLOUDINARY 🚨")
    
    # Set environment variables
    os.environ['CLOUDINARY_CLOUD_NAME'] = 'dzecfjfju'
    os.environ['CLOUDINARY_API_KEY'] = '853483899852935' 
    os.environ['CLOUDINARY_API_SECRET'] = 'tFJ6Rb9xofDzV2Y1YrBZWaIZkhs'
    
    # Sample product image URLs (placeholder images)
    sample_images = {
        'electronics': 'https://images.unsplash.com/photo-1498049794561-7780e7231661?w=400',
        'fashion': 'https://images.unsplash.com/photo-1441986300917-64674bd600d8?w=400',
        'fitness': 'https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=400',
        'home': 'https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=400',
        'beauty': 'https://images.unsplash.com/photo-1596462502278-27bfdc403348?w=400'
    }
    
    # Category mapping for products
    category_mapping = {
        'resistance': 'fitness', 'band': 'fitness', 'fitness': 'fitness',
        'iphone': 'electronics', 'samsung': 'electronics', 'sony': 'electronics', 'philips': 'electronics', 'led': 'electronics',
        't-shirt': 'fashion', 'coat': 'fashion', 'jacket': 'fashion', 'adidas': 'fashion', 'nike': 'fashion',
        'bottle': 'home', 'tea': 'home', 'lamp': 'home',
        'headphones': 'electronics'
    }
    
    products = Product.objects.exclude(image='').exclude(image__isnull=True)
    migrated = 0
    
    for product in products:
        try:
            print(f"\n🔄 Processing: {product.name}")
            
            # Skip if already using Cloudinary
            if 'cloudinary.com' in str(product.image):
                print("  ✅ Already using Cloudinary")
                continue
            
            # Determine category
            category = 'electronics'  # default
            name_lower = product.name.lower()
            for keyword, cat in category_mapping.items():
                if keyword in name_lower:
                    category = cat
                    break
            
            # Download sample image
            image_url = sample_images[category]
            response = requests.get(image_url)
            
            if response.status_code == 200:
                # Upload to Cloudinary
                result = cloudinary.uploader.upload(
                    response.content,
                    folder='products',
                    public_id=f"product_{product.id}_{product.name.lower().replace(' ', '_').replace('&', 'and')[:30]}",
                    overwrite=True,
                    resource_type='image'
                )
                
                if result.get('public_id'):
                    # Update product with Cloudinary public_id
                    product.image = result['public_id']
                    product.save()
                    migrated += 1
                    print(f"  ✅ UPLOADED: {result['secure_url']}")
                else:
                    print(f"  ❌ Upload failed")
            else:
                print(f"  ❌ Failed to download sample image")
                
        except Exception as e:
            print(f"  ❌ ERROR: {str(e)}")
    
    print(f"\n🎯 UPLOAD SUMMARY:")
    print(f"✅ Successfully uploaded: {migrated}")
    print(f"📊 Total products: {products.count()}")

if __name__ == "__main__":
    upload_sample_images()
