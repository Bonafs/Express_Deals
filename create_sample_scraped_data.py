#!/usr/bin/env python
"""
Populate sample scraped product data with real product images
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'express_deals.settings')
django.setup()

from scraping.models import ScrapedProduct, ScrapeJob, ScrapeTarget
from products.models import Product, Category
from decimal import Decimal


def create_sample_scraped_data():
    """Create sample scraped product data with real product images"""
    
    # Real product data with actual image URLs (publicly available)
    sample_products = [
        {
            'title': 'Sony PlayStation 5 Console',
            'price': Decimal('449.99'),
            'original_price': Decimal('499.99'),
            'image_url': 'https://images.unsplash.com/photo-1606813907291-d86efa9b94db?w=400&h=400&fit=crop',
            'product_url': 'https://example.com/ps5',
            'description': 'Latest PlayStation 5 gaming console with ultra-high speed SSD',
            'brand': 'Sony',
            'availability': 'In Stock'
        },
        {
            'title': 'Royal Doulton Fine Bone China Tea Set',
            'price': Decimal('129.99'),
            'original_price': Decimal('179.99'),
            'image_url': 'https://images.unsplash.com/photo-1544787219-7f47ccb76574?w=400&h=400&fit=crop',
            'product_url': 'https://example.com/tea-set',
            'description': 'Elegant fine bone china tea set with floral pattern',
            'brand': 'Royal Doulton',
            'availability': 'In Stock'
        },
        {
            'title': 'Barbour Classic Bedale Wax Jacket',
            'price': Decimal('239.99'),
            'original_price': Decimal('279.99'),
            'image_url': 'https://images.unsplash.com/photo-1551232864-3f0890e580d9?w=400&h=400&fit=crop',
            'product_url': 'https://example.com/barbour-jacket',
            'description': 'Classic British wax jacket, perfect for countryside adventures',
            'brand': 'Barbour',
            'availability': 'In Stock'
        },
        {
            'title': 'Dyson V15 Detect Absolute Vacuum Cleaner',
            'price': Decimal('599.99'),
            'original_price': Decimal('699.99'),
            'image_url': 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400&h=400&fit=crop',
            'product_url': 'https://example.com/dyson-v15',
            'description': 'Advanced cordless vacuum with laser dust detection',
            'brand': 'Dyson',
            'availability': 'In Stock'
        },
        {
            'title': 'Nike Air Max UK Limited Edition Sneakers',
            'price': Decimal('129.99'),
            'original_price': Decimal('159.99'),
            'image_url': 'https://images.unsplash.com/photo-1549298916-b41d501d3772?w=400&h=400&fit=crop',
            'product_url': 'https://example.com/nike-air-max',
            'description': 'Limited edition UK-inspired Air Max sneakers',
            'brand': 'Nike',
            'availability': 'In Stock'
        },
        {
            'title': 'Cambridge Satchel Classic Leather Bag',
            'price': Decimal('189.99'),
            'original_price': Decimal('229.99'),
            'image_url': 'https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=400&h=400&fit=crop',
            'product_url': 'https://example.com/cambridge-satchel',
            'description': 'Handcrafted leather satchel made in Cambridge, England',
            'brand': 'Cambridge Satchel',
            'availability': 'In Stock'
        },
        {
            'title': 'Molton Brown London Luxury Bath Set',
            'price': Decimal('89.99'),
            'original_price': Decimal('119.99'),
            'image_url': 'https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=400&h=400&fit=crop',
            'product_url': 'https://example.com/molton-brown',
            'description': 'Luxury bath and body care set with British botanicals',
            'brand': 'Molton Brown',
            'availability': 'In Stock'
        },
        {
            'title': 'Wedgwood Jasperware Vase Collection',
            'price': Decimal('149.99'),
            'original_price': Decimal('199.99'),
            'image_url': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=400&h=400&fit=crop',
            'product_url': 'https://example.com/wedgwood-vase',
            'description': 'Classic Wedgwood jasperware vase with iconic blue design',
            'brand': 'Wedgwood',
            'availability': 'Limited Stock'
        }
    ]
    
    # Create or get scrape target
    scrape_target, created = ScrapeTarget.objects.get_or_create(
        name='UK Premium Retailers',
        defaults={
            'site_type': 'custom',
            'base_url': 'https://example-uk-retailer.com',
            'search_url_template': 'https://example-uk-retailer.com/search?q={query}',
            'product_selector': '.product-item',
            'title_selector': '.product-title',
            'price_selector': '.price',
            'image_selector': '.product-image img',
            'url_selector': '.product-link'
        }
    )
    
    # Create scrape job
    scrape_job = ScrapeJob.objects.create(
        target=scrape_target,
        status='completed',
        search_query='premium uk products',
        products_found=len(sample_products),
        products_imported=len(sample_products)
    )
    
    print(f"Creating {len(sample_products)} sample scraped products...")
    
    created_count = 0
    for i, product_data in enumerate(sample_products):
        scraped_product, created = ScrapedProduct.objects.get_or_create(
            job=scrape_job,
            external_id=f'sample_{i+1}',
            defaults=product_data
        )
        
        if created:
            created_count += 1
            print(f"  ✓ Created: {scraped_product.title}")
        else:
            print(f"  - Exists: {scraped_product.title}")
    
    print(f"\n=== Summary ===")
    print(f"Created {created_count} new scraped products")
    print(f"Total scraped products: {ScrapedProduct.objects.count()}")
    
    return created_count


def main():
    """Main function"""
    print("Express Deals - Sample Scraped Data Creator\n")
    create_sample_scraped_data()
    print("\n=== Sample Data Creation Complete ===")


if __name__ == "__main__":
    main()
