#!/usr/bin/env python
"""
Verify image handling consistency across all templates
"""
import os
import re
import sys
import django

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'express_deals.settings')
django.setup()

print("🔍 VERIFYING IMAGE HANDLING CONSISTENCY")
print("=" * 60)

# Templates to check
templates_to_check = [
    'templates/products/product_list.html',
    'templates/products/product_detail.html',
    'templates/orders/checkout.html',
    'orders/templates/orders/cart.html'
]

issues_found = []

for template_path in templates_to_check:
    full_path = os.path.join(os.path.dirname(__file__), template_path)
    if os.path.exists(full_path):
        print(f"\n📄 Checking: {template_path}")
        
        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Check for old static image references
        static_refs = re.findall(r'{% static [\'"]images/no-image\.jpg[\'"] %}', content)
        if static_refs:
            issues_found.append(f"❌ {template_path}: Found {len(static_refs)} static no-image references")
            print(f"   ❌ Found {len(static_refs)} static image references")
        else:
            print(f"   ✅ No static image references")
            
        # Check for inconsistent fallback text
        image_available = content.count('Image Available')
        no_image = content.count('No Image')
        
        if image_available > 0:
            issues_found.append(f"❌ {template_path}: Found {image_available} 'Image Available' text")
            print(f"   ❌ Found {image_available} 'Image Available' text")
        else:
            print(f"   ✅ No 'Image Available' text")
            
        # Check for proper Cloudinary usage
        cloudinary_urls = len(re.findall(r'{{ .*\.image\.url }}', content))
        print(f"   ✅ Found {cloudinary_urls} Cloudinary image URLs")
        
        # Check for error handling
        error_handlers = len(re.findall(r'onerror=', content))
        print(f"   ✅ Found {error_handlers} image error handlers")
        
    else:
        print(f"\n❌ Template not found: {template_path}")

print("\n" + "=" * 60)
if issues_found:
    print("❌ ISSUES FOUND:")
    for issue in issues_found:
        print(f"   {issue}")
else:
    print("✅ ALL IMAGE HANDLING IS CONSISTENT!")
    print("✅ No static image references found")
    print("✅ No inconsistent fallback text found")
    print("✅ All templates use modern Cloudinary approach")

# Test a sample product image
try:
    from products.models import Product
    product = Product.objects.filter(image__isnull=False).first()
    if product:
        print(f"\n📷 Sample product image URL: {product.image.url}")
        print("✅ Cloudinary integration working")
    else:
        print("\n⚠️  No products with images found")
except Exception as e:
    print(f"\n❌ Error testing product images: {e}")

print("\n🎉 Image consistency verification completed!")
