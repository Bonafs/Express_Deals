import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'express_deals.settings')
django.setup()

from products.models import Product, Category

# Check products
total = Product.objects.count()
with_images = Product.objects.exclude(image='').exclude(image__isnull=True).count()
featured = Product.objects.filter(is_featured=True).count()

print(f"📊 FINAL STATUS:")
print(f"   Total Products: {total}")
print(f"   Products with Images: {with_images}")
print(f"   Featured Products: {featured}")
print(f"   Image Success Rate: {(with_images/total*100):.1f}%" if total > 0 else "   No products found")

if total > 0:
    print(f"\n🎯 SAMPLE PRODUCTS:")
    for product in Product.objects.all()[:5]:
        image_status = "🖼️" if product.image else "❌"
        featured_status = "⭐" if product.is_featured else "📦"
        print(f"   {featured_status}{image_status} {product.name} - £{product.price}")
        
    print(f"\n📋 BY CATEGORY:")
    for category in Category.objects.all():
        count = Product.objects.filter(category=category).count()
        if count > 0:
            print(f"   {category.name}: {count} products")
else:
    print("❌ No products found! Script may have failed.")
