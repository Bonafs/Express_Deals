#!/usr/bin/env python
"""
Script to fix production issues with Cloudinary and static files.
"""

import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'express_deals.settings')
django.setup()

def upload_default_image():
    """Upload a default product image to Cloudinary."""
    print("🖼️  Uploading default product image to Cloudinary...")
    print("=" * 60)
    
    try:
        import cloudinary.uploader
        from PIL import Image
        import io
        
        # Create a simple default image
        img = Image.new('RGB', (400, 400), color='#f0f0f0')
        from PIL import ImageDraw, ImageFont
        
        draw = ImageDraw.Draw(img)
        
        # Add text to the image
        text = "No Image\nAvailable"
        
        # Try to use a default font, fall back if not available
        try:
            font = ImageFont.truetype("arial.ttf", 36)
        except:
            font = ImageFont.load_default()
        
        # Calculate text position for centering
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        position = ((400 - text_width) // 2, (400 - text_height) // 2)
        
        draw.text(position, text, fill='#666666', font=font, align='center')
        
        # Save to bytes
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='JPEG', quality=85)
        img_bytes.seek(0)
        
        # Upload to Cloudinary
        result = cloudinary.uploader.upload(
            img_bytes.getvalue(),
            public_id="products/default",
            folder="products",
            overwrite=True,
            resource_type="image"
        )
        
        print(f"✅ Default image uploaded successfully!")
        print(f"   Public ID: {result['public_id']}")
        print(f"   URL: {result['secure_url']}")
        print(f"   Format: {result['format']}")
        print(f"   Size: {result['width']}x{result['height']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error uploading default image: {e}")
        return False

def check_static_files():
    """Check static files configuration."""
    print("\n📁 Checking static files configuration...")
    print("=" * 60)
    
    try:
        from django.conf import settings
        from django.contrib.staticfiles import finders
        import os
        
        print(f"📍 STATIC_URL: {settings.STATIC_URL}")
        print(f"📍 STATIC_ROOT: {getattr(settings, 'STATIC_ROOT', 'Not set')}")
        print(f"📍 STATICFILES_STORAGE: {getattr(settings, 'STATICFILES_STORAGE', 'Default')}")
        
        # Check if main CSS file exists
        css_file = finders.find('css/style.css')
        if css_file:
            print(f"✅ Main CSS file found: {css_file}")
            
            # Check file size
            if os.path.exists(css_file):
                size = os.path.getsize(css_file)
                print(f"   Size: {size} bytes")
            
        else:
            print("❌ Main CSS file not found!")
            
        # List available CSS files
        print("\n📝 Available CSS files:")
        css_files = finders.find('css/', all=True)
        if css_files:
            for css_file in css_files:
                if os.path.isfile(css_file):
                    print(f"   - {css_file}")
        else:
            print("   No CSS files found!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error checking static files: {e}")
        return False

def verify_cloudinary_settings():
    """Verify Cloudinary settings are properly loaded."""
    print("\n☁️  Verifying Cloudinary settings...")
    print("=" * 60)
    
    try:
        import cloudinary
        from django.conf import settings
        
        config = cloudinary.config()
        
        print(f"✅ Cloud Name: {config.cloud_name}")
        print(f"✅ API Key: {config.api_key}")
        print(f"✅ Secure: {config.secure}")
        
        # Check Django settings
        cloudinary_storage = getattr(settings, 'CLOUDINARY_STORAGE', {})
        print(f"✅ Django CLOUDINARY_STORAGE: {bool(cloudinary_storage)}")
        
        print(f"✅ DEFAULT_FILE_STORAGE: {getattr(settings, 'DEFAULT_FILE_STORAGE', 'Not set')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error verifying Cloudinary settings: {e}")
        return False

def test_image_urls():
    """Test that product image URLs are working."""
    print("\n🔗 Testing product image URLs...")
    print("=" * 60)
    
    try:
        from products.models import Product
        
        # Test a few products
        products = Product.objects.filter(image__isnull=False)[:3]
        
        for product in products:
            print(f"\n📦 Product: {product.name}")
            if product.image:
                url = product.image.url
                print(f"   Image URL: {url}")
                
                # Test if URL is accessible
                import requests
                try:
                    response = requests.head(url, timeout=10)
                    if response.status_code == 200:
                        print(f"   ✅ URL accessible (Status: {response.status_code})")
                    else:
                        print(f"   ⚠️  URL returned status: {response.status_code}")
                except requests.RequestException as e:
                    print(f"   ❌ URL not accessible: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing image URLs: {e}")
        return False

def main():
    """Run all production fixes."""
    print("🚀 Express Deals - Production Issues Fix")
    print("=" * 70)
    
    success_count = 0
    total_tasks = 4
    
    # Run all checks and fixes
    if verify_cloudinary_settings():
        success_count += 1
    
    if upload_default_image():
        success_count += 1
        
    if check_static_files():
        success_count += 1
        
    if test_image_urls():
        success_count += 1
    
    print("\n" + "=" * 70)
    if success_count == total_tasks:
        print("🎉 ALL FIXES COMPLETED SUCCESSFULLY!")
        print("   Your production issues should now be resolved.")
        print("   Try accessing your Heroku site again.")
    else:
        print(f"⚠️  {success_count}/{total_tasks} tasks completed successfully.")
        print("   Some issues may need manual attention.")
    
    return success_count == total_tasks

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
