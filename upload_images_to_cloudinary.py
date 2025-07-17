#!/usr/bin/env python3
"""
Upload local product images to Cloudinary and update database
"""
import os
import django
from pathlib import Path

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'express_deals.settings')
django.setup()

from products.models import Product
from django.db import models
import cloudinary.uploader
import cloudinary.api


def upload_product_images():
    """Upload all local product images to Cloudinary"""
    print("🚀 Starting Cloudinary upload...")
    
    # Get the products directory
    products_dir = Path(__file__).parent / 'products'
    
    # Get all JPG files
    image_files = list(products_dir.glob('*.jpg'))
    print(f"📁 Found {len(image_files)} image files")
    
    uploaded_count = 0
    
    for image_path in image_files:
        try:
            print(f"📤 Uploading {image_path.name}...")
            
            # Upload to Cloudinary
            result = cloudinary.uploader.upload(
                str(image_path),
                public_id=f"products/{image_path.stem}",
                folder="products",
                overwrite=True,
                resource_type="image"
            )
            
            print(f"✅ Uploaded: {result['public_id']}")
            print(f"🔗 URL: {result['secure_url']}")
            
            # Update any products that use this image
            image_name = image_path.name
            # Also try without extension for more flexible matching
            image_stem = image_path.stem
            
            products = Product.objects.filter(
                models.Q(image__icontains=image_name) | 
                models.Q(image__icontains=image_stem)
            )
            
            for product in products:
                try:
                    # Update the image field with Cloudinary URL
                    try:
                        old_image = str(product.image) if product.image else "None"
                    except (AttributeError, Exception):
                        old_image = "No image"
                    
                    product.image = f"products/{image_path.stem}.jpg"
                    product.save()
                    print(f"📝 Updated product '{product.name}': {old_image} -> {product.image}")
                    
                except Exception as e:
                    print(f"⚠️  Error updating product '{product.name}': {e}")
            
            uploaded_count += 1
            
        except Exception as e:
            print(f"❌ Error uploading {image_path.name}: {e}")
    
    print(f"\n🎉 Upload complete! {uploaded_count}/{len(image_files)} images uploaded")


if __name__ == "__main__":
    upload_product_images()
