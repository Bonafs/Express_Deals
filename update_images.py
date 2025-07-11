#!/usr/bin/env python
"""
Image Update Utility for Express Deals
Updates product images from scraped data or fetches from external sources
"""

import os
import sys
import django
import requests
from urllib.parse import urlparse
from PIL import Image
import tempfile

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'express_deals.settings')
django.setup()

from products.models import Product
from scraping.models import ScrapedProduct
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.db import models


def download_image_from_url(url, product_name):
    """Download image from URL and return ContentFile"""
    try:
        # Headers to avoid being blocked
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Get file extension from URL
        parsed_url = urlparse(url)
        path = parsed_url.path
        ext = path.split('.')[-1] if '.' in path else 'jpg'
        
        # Ensure valid image extension
        if ext.lower() not in ['jpg', 'jpeg', 'png', 'webp']:
            ext = 'jpg'
        
        # Clean product name for filename
        clean_name = "".join(c for c in product_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
        clean_name = clean_name.replace(' ', '_')[:50]  # Limit length
        
        filename = f"{clean_name}.{ext}"
        
        return ContentFile(response.content, name=filename)
        
    except Exception as e:
        print(f"Error downloading image from {url}: {str(e)}")
        return None


def update_product_images_from_scraped_data():
    """Update product images using scraped product data"""
    print("=== Updating Product Images from Scraped Data ===")
    
    updated_count = 0
    error_count = 0
    
    # Get all products that need images or have placeholder images
    products_needing_images = Product.objects.all()
    
    print(f"Checking {products_needing_images.count()} products for image updates")
    
    for product in products_needing_images:
        print(f"\nProcessing: {product.name}")
        
        # Try multiple matching strategies for scraped products
        scraped_products = []
        
        # Strategy 1: Exact name match
        scraped_products = ScrapedProduct.objects.filter(
            title__iexact=product.name
        ).order_by('-scraped_at')
        
        # Strategy 2: Contains product name (case insensitive)
        if not scraped_products.exists():
            scraped_products = ScrapedProduct.objects.filter(
                title__icontains=product.name.split()[0]  # First word match
            ).order_by('-scraped_at')
        
        # Strategy 3: Product name contains scraped title
        if not scraped_products.exists():
            for scraped in ScrapedProduct.objects.filter(image_url__isnull=False)[:20]:
                if any(word.lower() in product.name.lower() for word in scraped.title.split()[:3]):
                    scraped_products = [scraped]
                    break
        
        # Strategy 4: Category-based matching
        if not scraped_products and product.category:
            category_keywords = {
                'Electronics': ['PlayStation', 'Xbox', 'Nintendo', 'Apple', 'Samsung', 'Sony'],
                'Clothing': ['Jacket', 'Shirt', 'Dress', 'Shoes', 'Barbour', 'Nike'],
                'Home': ['Tea Set', 'Furniture', 'Dyson', 'Kitchen'],
                'Beauty': ['Skincare', 'Makeup', 'Perfume'],
                'Sports': ['Nike', 'Adidas', 'Fitness', 'Sports']
            }
            
            keywords = category_keywords.get(product.category.name, [])
            for keyword in keywords:
                if keyword.lower() in product.name.lower():
                    scraped_products = ScrapedProduct.objects.filter(
                        title__icontains=keyword,
                        image_url__isnull=False
                    ).order_by('-scraped_at')[:1]
                    if scraped_products.exists():
                        break
        
        # Use the best match
        if scraped_products:
            if hasattr(scraped_products, 'first'):
                scraped = scraped_products.first()
            else:
                scraped = scraped_products[0]
                
            if scraped.image_url:
                print(f"  Found scraped image: {scraped.image_url}")
                print(f"  Scraped title: {scraped.title}")
                
                # Download and save image
                image_file = download_image_from_url(scraped.image_url, product.name)
                if image_file:
                    product.image.save(image_file.name, image_file, save=True)
                    updated_count += 1
                    print(f"  ✓ Updated image for {product.name}")
                    
                    # Link the scraped product to the imported product
                    scraped.imported_product = product
                    scraped.is_processed = True
                    scraped.save()
                else:
                    error_count += 1
                    print(f"  ✗ Failed to download image for {product.name}")
            else:
                print(f"  No image URL in scraped data")
        else:
            print(f"  No matching scraped product found")
    
    print(f"\n=== Summary ===")
    print(f"Updated: {updated_count} products")
    print(f"Errors: {error_count} products")


def update_images_from_placeholder_service():
    """Update product images using a placeholder service with product-relevant images"""
    print("=== Updating Product Images from Placeholder Service ===")
    
    # Mapping of categories to relevant image keywords
    category_keywords = {
        'electronics': ['technology', 'gadget', 'device'],
        'clothing': ['fashion', 'apparel', 'style'],
        'home': ['furniture', 'decor', 'interior'],
        'beauty': ['cosmetics', 'skincare', 'beauty'],
        'sports': ['fitness', 'sport', 'exercise'],
        'books': ['book', 'reading', 'literature'],
        'toys': ['toy', 'children', 'play'],
        'food': ['food', 'cuisine', 'meal'],
        'automotive': ['car', 'vehicle', 'automotive'],
        'garden': ['garden', 'plant', 'nature']
    }
    
    updated_count = 0
    
    # Get products without proper images
    products_needing_images = Product.objects.filter(
        models.Q(image='') | 
        models.Q(image='products/default.jpg') |
        models.Q(image__isnull=True)
    )
    
    print(f"Found {products_needing_images.count()} products needing images")
    
    for product in products_needing_images:
        print(f"\nProcessing: {product.name}")
        
        # Determine category keyword
        category_name = product.category.name.lower() if product.category else 'product'
        keyword = 'product'  # default
        
        for cat, keywords in category_keywords.items():
            if cat in category_name:
                keyword = keywords[0]
                break
        
        # Use Unsplash or similar service for better images
        # For demo, using picsum with category-specific dimensions
        width, height = 400, 400
        if 'electronics' in category_name:
            width, height = 500, 400
        elif 'clothing' in category_name:
            width, height = 400, 500
        
        # Generate image URL (using picsum as it's free and reliable)
        image_url = f"https://picsum.photos/{width}/{height}?random={product.id}"
        
        print(f"  Using placeholder: {image_url}")
        
        # Download and save image
        image_file = download_image_from_url(image_url, f"{product.name}_{keyword}")
        if image_file:
            product.image.save(image_file.name, image_file, save=True)
            updated_count += 1
            print(f"  ✓ Updated placeholder image for {product.name}")
        else:
            print(f"  ✗ Failed to download placeholder image for {product.name}")
    
    print(f"\n=== Summary ===")
    print(f"Updated: {updated_count} products with placeholder images")


def main():
    """Main function to update product images"""
    print("Express Deals - Image Update Utility\n")
    
    # First try to update from scraped data
    try:
        update_product_images_from_scraped_data()
    except Exception as e:
        print(f"Error updating from scraped data: {e}")
    
    # Then update remaining with placeholder service
    try:
        update_images_from_placeholder_service()
    except Exception as e:
        print(f"Error updating with placeholder service: {e}")
    
    print("\n=== Image Update Complete ===")


if __name__ == "__main__":
    main()
