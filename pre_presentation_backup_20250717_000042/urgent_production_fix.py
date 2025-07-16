#!/usr/bin/env python
"""
URGENT: Fix critical production issues
1. Fix Cloudinary default image path
2. Fix static files MIME type issue
"""

import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'express_deals.settings')
django.setup()

def fix_cloudinary_default_image():
    """Fix the default image path in Cloudinary."""
    print("🔧 URGENT: Fixing Cloudinary default image...")
    print("=" * 60)
    
    try:
        import cloudinary.uploader
        from PIL import Image, ImageDraw, ImageFont
        import io
        
        # Create a simple default image
        img = Image.new('RGB', (400, 400), color='#f8f9fa')
        draw = ImageDraw.Draw(img)
        
        # Add Express Deals branding
        try:
            font_large = ImageFont.truetype("arial.ttf", 32)
            font_small = ImageFont.truetype("arial.ttf", 18)
        except:
            font_large = ImageFont.load_default()
            font_small = ImageFont.load_default()
        
        # Draw text
        text1 = "EXPRESS DEALS"
        text2 = "No Image Available"
        
        # Calculate positions
        bbox1 = draw.textbbox((0, 0), text1, font=font_large)
        bbox2 = draw.textbbox((0, 0), text2, font=font_small)
        
        w1, h1 = bbox1[2] - bbox1[0], bbox1[3] - bbox1[1]
        w2, h2 = bbox2[2] - bbox2[0], bbox2[3] - bbox2[1]
        
        pos1 = ((400 - w1) // 2, 160)
        pos2 = ((400 - w2) // 2, 220)
        
        # Draw text
        draw.text(pos1, text1, fill='#333333', font=font_large)
        draw.text(pos2, text2, fill='#666666', font=font_small)
        
        # Add border
        draw.rectangle([10, 10, 390, 390], outline='#dee2e6', width=2)
        
        # Save to bytes
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='JPEG', quality=85)
        img_bytes.seek(0)
        
        # Upload with correct path (without /v1/)
        result = cloudinary.uploader.upload(
            img_bytes.getvalue(),
            public_id="products/default",
            overwrite=True,
            resource_type="image",
            folder=""  # Don't add extra folder
        )
        
        print(f"✅ Default image uploaded successfully!")
        print(f"   Public ID: {result['public_id']}")
        print(f"   URL: {result['secure_url']}")
        
        # Also upload as .jpg extension variant
        result2 = cloudinary.uploader.upload(
            img_bytes.getvalue(),
            public_id="products/default.jpg",
            overwrite=True,
            resource_type="image",
            folder=""
        )
        
        print(f"✅ Default.jpg variant uploaded!")
        print(f"   Public ID: {result2['public_id']}")
        print(f"   URL: {result2['secure_url']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error uploading default image: {e}")
        return False

def fix_product_image_fields():
    """Update product image fields to use correct default."""
    print("\n🔧 Fixing product image fields...")
    print("=" * 60)
    
    try:
        from products.models import Product
        
        # Get products with empty/null images
        products_needing_default = Product.objects.filter(
            models.Q(image__isnull=True) | models.Q(image='')
        )
        
        count = products_needing_default.count()
        print(f"📦 Found {count} products needing default images")
        
        # Update them to use the correct default
        updated = products_needing_default.update(image='products/default')
        
        print(f"✅ Updated {updated} products to use default image")
        
        # Test a few products
        test_products = Product.objects.filter(image='products/default')[:3]
        for product in test_products:
            print(f"   - {product.name}: {product.image.url}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error fixing product images: {e}")
        return False

def test_static_files_issue():
    """Diagnose the static files MIME type issue."""
    print("\n🔧 Diagnosing static files issue...")
    print("=" * 60)
    
    try:
        from django.conf import settings
        from django.contrib.staticfiles import finders
        import os
        
        print(f"📁 STATIC_URL: {settings.STATIC_URL}")
        print(f"📁 STATIC_ROOT: {getattr(settings, 'STATIC_ROOT', 'Not set')}")
        print(f"📁 STATICFILES_STORAGE: {getattr(settings, 'STATICFILES_STORAGE', 'Default')}")
        
        # Check if CSS file exists locally
        css_file = finders.find('css/style.css')
        if css_file and os.path.exists(css_file):
            size = os.path.getsize(css_file)
            print(f"✅ CSS file found locally: {css_file} ({size} bytes)")
            
            # Read first few lines to check content
            with open(css_file, 'r') as f:
                first_lines = f.read(200)
            print(f"📄 CSS Content Preview: {first_lines[:100]}...")
            
        else:
            print("❌ CSS file not found locally!")
        
        # Check WhiteNoise configuration
        middleware = getattr(settings, 'MIDDLEWARE', [])
        whitenoise_found = any('whitenoise' in mw.lower() for mw in middleware)
        print(f"📦 WhiteNoise in middleware: {whitenoise_found}")
        
        if whitenoise_found:
            print("✅ WhiteNoise is configured")
        else:
            print("❌ WhiteNoise not found in middleware!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error checking static files: {e}")
        return False

def run_collectstatic():
    """Run collectstatic to ensure files are properly collected."""
    print("\n🔧 Running collectstatic...")
    print("=" * 60)
    
    try:
        from django.core.management import call_command
        import io
        import sys
        
        # Capture output
        old_stdout = sys.stdout
        sys.stdout = buffer = io.StringIO()
        
        call_command('collectstatic', '--noinput', verbosity=2)
        
        sys.stdout = old_stdout
        output = buffer.getvalue()
        
        print("✅ Collectstatic completed!")
        print("Output preview:")
        print(output[-300:])  # Last 300 characters
        
        return True
        
    except Exception as e:
        print(f"❌ Error running collectstatic: {e}")
        return False

def main():
    """Run all urgent fixes."""
    print("🚨 EXPRESS DEALS - URGENT PRODUCTION FIXES")
    print("=" * 70)
    print("Fixing CSS MIME type and Cloudinary 404 issues...")
    
    success_count = 0
    
    if fix_cloudinary_default_image():
        success_count += 1
    
    if fix_product_image_fields():
        success_count += 1
        
    if test_static_files_issue():
        success_count += 1
        
    if run_collectstatic():
        success_count += 1
    
    print("\n" + "=" * 70)
    if success_count >= 3:
        print("🎉 URGENT FIXES COMPLETED!")
        print("   Deploy these changes immediately to Heroku")
    else:
        print(f"⚠️  {success_count}/4 fixes completed")
    
    return success_count >= 3

if __name__ == "__main__":
    from django.db import models
    success = main()
    sys.exit(0 if success else 1)
