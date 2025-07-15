#!/usr/bin/env python
"""
Test script to verify Cloudinary configuration is working properly.
"""

import os
import sys
import django

# Add the project directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'express_deals.settings')
django.setup()

def test_cloudinary_config():
    """Test if Cloudinary is properly configured."""
    print("Testing Cloudinary Configuration...")
    print("=" * 50)
    
    try:
        # Import cloudinary after Django setup
        import cloudinary
        from express_deals import cloudinary_settings
        
        # Check if cloudinary is configured
        config = cloudinary.config()
        print(f"✅ Cloudinary Cloud Name: {config.cloud_name}")
        print(f"✅ Cloudinary API Key: {config.api_key}")
        print(f"✅ Cloudinary Secure: {config.secure}")
        
        # Test image transformations
        from express_deals.cloudinary_settings import get_product_image_url, PRODUCT_IMAGE_TRANSFORMATIONS
        
        print("\n📸 Image Transformation Presets:")
        for preset_name, preset_config in PRODUCT_IMAGE_TRANSFORMATIONS.items():
            print(f"  - {preset_name}: {preset_config['width']}x{preset_config['height']}")
        
        # Test URL generation
        test_public_id = "products/test_image"
        test_url = get_product_image_url(test_public_id, 'medium')
        print(f"\n🔗 Test Image URL: {test_url}")
        
        print("\n✅ Cloudinary configuration is working properly!")
        return True
        
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        return False
    except Exception as e:
        print(f"❌ Configuration Error: {e}")
        return False

def test_product_images():
    """Test if products have images and can generate URLs."""
    print("\n🛍️  Testing Product Images...")
    print("=" * 50)
    
    try:
        from products.models import Product
        
        # Get first few products with images
        products_with_images = Product.objects.filter(image__isnull=False)[:5]
        
        if not products_with_images.exists():
            print("⚠️  No products with images found in database")
            return False
        
        print(f"📦 Found {products_with_images.count()} products with images")
        
        for product in products_with_images:
            print(f"\n  Product: {product.name}")
            print(f"  Image Field: {product.image}")
            if product.image:
                print(f"  Image URL: {product.image.url}")
                print(f"  Image Name: {product.image.name}")
            
        print("\n✅ Product images are properly configured!")
        return True
        
    except Exception as e:
        print(f"❌ Product Image Error: {e}")
        return False

def main():
    """Run all tests."""
    print("🚀 Express Deals - Cloudinary Configuration Test")
    print("=" * 60)
    
    cloudinary_ok = test_cloudinary_config()
    product_images_ok = test_product_images()
    
    print("\n" + "=" * 60)
    if cloudinary_ok and product_images_ok:
        print("🎉 ALL TESTS PASSED! Cloudinary is properly configured.")
        print("   Images should now be rendering in the ProductListView.")
    else:
        print("❌ SOME TESTS FAILED. Please check the configuration.")
    
    return cloudinary_ok and product_images_ok

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
