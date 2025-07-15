import os
import django
import requests

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'express_deals.settings')
os.environ['CLOUDINARY_CLOUD_NAME'] = 'dzecfjfju'
os.environ['CLOUDINARY_API_KEY'] = '853483899852935'
os.environ['CLOUDINARY_API_SECRET'] = 'tFJ6Rb9xofDzV2Y1YrBZWaIZkhs'
django.setup()

from products.models import Product
import cloudinary
import cloudinary.uploader

def fix_all_images():
    """Fix all product images by uploading placeholder images to Cloudinary"""
    print("🚨 FIXING ALL PRODUCT IMAGES 🚨")
    
    # Sample product image URL (we'll use this as a placeholder)
    sample_image_url = "https://via.placeholder.com/600x400/2563eb/ffffff?text=Express+Deals+Product"
    
    products = Product.objects.exclude(image='').exclude(image__isnull=True)
    
    for product in products:
        try:
            print(f"🔄 Fixing: {product.name}")
            
            # Download the placeholder image
            response = requests.get(sample_image_url)
            if response.status_code == 200:
                
                # Upload to Cloudinary
                result = cloudinary.uploader.upload(
                    response.content,
                    folder='products',
                    public_id=f"product_{product.id}_{product.name.lower().replace(' ', '_')}",
                    overwrite=True,
                    resource_type='image'
                )
                
                if result.get('public_id'):
                    # Update product with Cloudinary public_id
                    product.image = result['public_id']
                    product.save()
                    print(f"  ✅ FIXED: {result['secure_url']}")
                else:
                    print(f"  ❌ Upload failed")
            else:
                print(f"  ❌ Could not download placeholder")
                
        except Exception as e:
            print(f"  ❌ ERROR: {str(e)}")
    
    print("🎯 ALL IMAGES FIXED!")

if __name__ == "__main__":
    fix_all_images()
