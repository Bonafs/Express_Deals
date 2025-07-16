import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'express_deals.settings')

# Set Cloudinary environment variables (for local testing only)
os.environ['CLOUDINARY_CLOUD_NAME'] = 'dzecfjfju'
os.environ['CLOUDINARY_API_KEY'] = '853483899852935'
os.environ['CLOUDINARY_API_SECRET'] = 'tFJ6Rb9xofDzV2Y1YrBZWaIZkhs'

django.setup()

from products.models import Product
import cloudinary
import cloudinary.uploader

def quick_migration():
    print("Starting Cloudinary migration...")
    
    products = Product.objects.exclude(image='')
    print(f"Found {products.count()} products with images")
    
    # Test first product
    if products.exists():
        product = products.first()
        print(f"\nTesting with: {product.name}")
        print(f"Current image: {product.image}")
        print(f"Current URL: {product.image.url}")
        
        # Test Cloudinary connection
        try:
            result = cloudinary.api.ping()
            print(f"Cloudinary connection: OK")
        except Exception as e:
            print(f"Cloudinary connection failed: {e}")
            return
        
        print("Migration test complete!")

if __name__ == "__main__":
    quick_migration()
