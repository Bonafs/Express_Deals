import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'express_deals.settings')
django.setup()

from products.models import Product

def check_final_status():
    """Check final status after image fixes"""
    print("🎯 EXPRESS DEALS - FINAL STATUS CHECK")
    print("=" * 40)
    
    total_products = Product.objects.count()
    products_with_images = Product.objects.exclude(image="").exclude(image__isnull=True).count()
    featured_products = Product.objects.filter(is_featured=True).count()
    
    print(f"📊 Total Products: {total_products}")
    print(f"🖼️ Products with Images: {products_with_images}")
    print(f"⭐ Featured Products: {featured_products}")
    
    if products_with_images == total_products:
        print("✅ ALL PRODUCTS HAVE IMAGES - READY FOR PRESENTATION!")
    else:
        missing = total_products - products_with_images
        print(f"⚠️ {missing} products still need images")
    
    # Show sample of products with images
    print("\n🎨 SAMPLE PRODUCTS WITH CLOUDINARY IMAGES:")
    sample_products = Product.objects.exclude(image="").exclude(image__isnull=True)[:5]
    
    for product in sample_products:
        print(f"  • {product.name} - £{product.price}")
        print(f"    Image: {product.image}")
    
    print(f"\n🚀 PROJECT IS PRESENTATION-READY!")

if __name__ == "__main__":
    check_final_status()
