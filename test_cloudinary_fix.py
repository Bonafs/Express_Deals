#!/usr/bin/env python3
"""
Test script to verify Cloudinary configuration is working properly
after fixing the empty cloudinary_settings.py file.
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'express_deals.settings')
django.setup()

def test_cloudinary_config():
    """Test if Cloudinary is properly configured"""
    print("🔧 Testing Cloudinary Configuration...")
    
    try:
        # Import cloudinary after Django setup
        import cloudinary
        from express_deals import cloudinary_settings
        
        # Test basic cloudinary config
        config = cloudinary.config()
        print(f"✅ Cloudinary Cloud Name: {config.cloud_name}")
        print(f"✅ Cloudinary API Key: {config.api_key[:8]}...")
        print(f"✅ Cloudinary API Secret: {'*' * 8}")
        
        # Test cloudinary_settings functions
        print("\n🔧 Testing Cloudinary Helper Functions...")
        
        # Test image URL generation
        test_public_id = "products/test_image"
        url = cloudinary_settings.get_product_image_url(test_public_id, 'medium')
        if url:
            print(f"✅ Image URL generation working: {url[:50]}...")
        else:
            print("❌ Image URL generation failed")
        
        # Test transformation presets
        transformations = cloudinary_settings.PRODUCT_IMAGE_TRANSFORMATIONS
        print(f"✅ Available transformations: {list(transformations.keys())}")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        return False
    except Exception as e:
        print(f"❌ Configuration Error: {e}")
        return False

def test_product_model():
    """Test if Product model can access images"""
    print("\n🔧 Testing Product Model Image Access...")
    
    try:
        from products.models import Product
        
        # Get a product with an image
        products_with_images = Product.objects.filter(image__isnull=False)[:1]
        
        if products_with_images:
            product = products_with_images[0]
            print(f"✅ Found product with image: {product.name}")
            print(f"✅ Image field value: {product.image}")
            
            if hasattr(product.image, 'url'):
                print(f"✅ Image URL accessible: {product.image.url}")
                return True
            else:
                print("❌ Image URL not accessible")
                return False
        else:
            print("⚠️  No products with images found in database")
            return True
            
    except Exception as e:
        print(f"❌ Product Model Error: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 Express Deals - Cloudinary Configuration Test")
    print("=" * 50)
    
    # Test 1: Cloudinary Configuration
    config_ok = test_cloudinary_config()
    
    # Test 2: Product Model
    model_ok = test_product_model()
    
    print("\n" + "=" * 50)
    if config_ok and model_ok:
        print("✅ ALL TESTS PASSED - Cloudinary is properly configured!")
        print("🎉 Images should now render in ProductListView")
    else:
        print("❌ SOME TESTS FAILED - Check the errors above")
    
    return config_ok and model_ok

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
