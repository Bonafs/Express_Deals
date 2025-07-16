#!/usr/bin/env python
"""
Test script to verify image rendering and Cloudinary configuration
"""

import os
import django
from django.conf import settings

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'express_deals.settings')
django.setup()

from products.models import Product
from express_deals import cloudinary_settings
import cloudinary

def test_cloudinary_config():
    """Test Cloudinary configuration"""
    print("=== Testing Cloudinary Configuration ===")
    
    # Check if cloudinary is configured
    config = cloudinary.config()
    print(f"Cloud Name: {config.cloud_name}")
    print(f"API Key: {config.api_key}")
    print(f"Secure: {config.secure}")
    print(f"Cloudinary configured: {'✓' if config.cloud_name else '✗'}")
    print()

def test_product_images():
    """Test product images"""
    print("=== Testing Product Images ===")
    
    # Get all products
    products = Product.objects.all()
    print(f"Total products: {products.count()}")
    
    # Check products with images
    products_with_images = products.exclude(image='')
    print(f"Products with images: {products_with_images.count()}")
    
    # Display first 5 products with images
    for i, product in enumerate(products_with_images[:5]):
        print(f"\n{i+1}. {product.name}")
        print(f"   Image field: {product.image}")
        if product.image:
            print(f"   Image URL: {product.image.url}")
            print(f"   Image name: {product.image.name}")
        else:
            print("   No image")
    
    print()

def test_media_settings():
    """Test media settings"""
    print("=== Testing Media Settings ===")
    print(f"DEFAULT_FILE_STORAGE: {settings.DEFAULT_FILE_STORAGE}")
    print(f"MEDIA_URL: {settings.MEDIA_URL}")
    print(f"CLOUDINARY_STORAGE: {getattr(settings, 'CLOUDINARY_STORAGE', 'Not set')}")
    print()

def main():
    """Main test function"""
    print("Express Deals - Image Rendering Test")
    print("====================================\n")
    
    test_cloudinary_config()
    test_media_settings() 
    test_product_images()
    
    print("Test completed!")

if __name__ == "__main__":
    main()
