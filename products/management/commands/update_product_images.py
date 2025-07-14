"""
Django management command to update product images from external sources
"""
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from django.db import models
from products.models import Product
from scraping.models import ScrapedProduct
import requests
from urllib.parse import urlparse
import tempfile


class Command(BaseCommand):
    help = 'Update product images from scraped data or external sources'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force update all images, even existing ones',
        )
        parser.add_argument(
            '--product-id',
            type=int,
            help='Update specific product by ID',
        )
        parser.add_argument(
            '--source',
            choices=['scraped', 'placeholder', 'unsplash'],
            default='scraped',
            help='Image source to use',
        )

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('Starting product image update...')
        )

        force_update = options['force']
        product_id = options.get('product_id')
        source = options['source']

        # Filter products
        queryset = Product.objects.all()
        if product_id:
            queryset = queryset.filter(id=product_id)
        
        if not force_update:
            queryset = queryset.filter(
                models.Q(image='') | 
                models.Q(image='') |
                models.Q(image__isnull=True)
            )

        self.stdout.write(f'Found {queryset.count()} products to update')

        updated_count = 0
        error_count = 0

        for product in queryset:
            self.stdout.write(f'Processing: {product.name}')
            
            try:
                if source == 'scraped':
                    success = self.update_from_scraped_data(product)
                elif source == 'placeholder':
                    success = self.create_placeholder_image(product)
                elif source == 'unsplash':
                    success = self.update_from_unsplash(product)
                else:
                    success = False

                if success:
                    updated_count += 1
                    self.stdout.write(
                        self.style.SUCCESS(f'  ✓ Updated {product.name}')
                    )
                else:
                    error_count += 1
                    self.stdout.write(
                        self.style.WARNING(f'  ⚠ Could not update {product.name}')
                    )

            except Exception as e:
                error_count += 1
                self.stdout.write(
                    self.style.ERROR(f'  ✗ Error updating {product.name}: {e}')
                )

        self.stdout.write(
            self.style.SUCCESS(
                f'\nCompleted! Updated: {updated_count}, Errors: {error_count}'
            )
        )

    def update_from_scraped_data(self, product):
        """Update product image from scraped data with improved matching"""
        # Try multiple matching strategies
        scraped_products = []
        
        # Strategy 1: Exact name match
        scraped_products = ScrapedProduct.objects.filter(
            title__iexact=product.name,
            image_url__isnull=False
        ).order_by('-scraped_at')
        
        # Strategy 2: Contains key words from product name
        if not scraped_products.exists():
            key_words = product.name.split()[:2]  # First 2 words
            for word in key_words:
                if len(word) > 3:  # Skip short words
                    scraped_products = ScrapedProduct.objects.filter(
                        title__icontains=word,
                        image_url__isnull=False
                    ).order_by('-scraped_at')
                    if scraped_products.exists():
                        break
        
        # Strategy 3: Brand matching if available
        if not scraped_products.exists() and hasattr(product, 'brand'):
            scraped_products = ScrapedProduct.objects.filter(
                models.Q(title__icontains=product.brand) | models.Q(brand__icontains=product.brand),
                image_url__isnull=False
            ).order_by('-scraped_at')

        if scraped_products.exists():
            scraped = scraped_products.first()
            if scraped.image_url:
                success = self.download_and_save_image(
                    scraped.image_url, 
                    product, 
                    f"scraped_{product.name}"
                )
                if success:
                    # Mark as processed and link
                    scraped.imported_product = product
                    scraped.is_processed = True
                    scraped.save()
                    return True
        return False

    def update_from_unsplash(self, product):
        """Update product image from Unsplash API"""
        # For demo purposes, using a simple approach
        # In production, you'd use Unsplash API with proper key
        category = product.category.name.lower() if product.category else 'product'
        
        # Map categories to search terms
        search_terms = {
            'electronics': 'technology',
            'clothing': 'fashion',
            'home': 'furniture',
            'beauty': 'cosmetics',
            'sports': 'fitness',
            'books': 'book',
            'toys': 'toy',
            'food': 'food',
            'automotive': 'car'
        }
        
        search_term = search_terms.get(category, 'product')
        
        # Using Lorem Picsum with category-specific sizing
        width, height = 400, 400
        image_url = f"https://picsum.photos/{width}/{height}?random={product.id}"
        
        return self.download_and_save_image(
            image_url, 
            product, 
            f"unsplash_{search_term}_{product.name}"
        )

    def create_placeholder_image(self, product):
        """Create a simple placeholder image"""
        # This would use PIL to create a custom placeholder
        # For now, return False to skip
        return False

    def download_and_save_image(self, url, product, base_filename):
        """Download image from URL and save to product"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()

            # Clean filename
            clean_name = "".join(c for c in base_filename if c.isalnum() or c in (' ', '-', '_'))
            clean_name = clean_name.replace(' ', '_')[:50]
            filename = f"{clean_name}.jpg"

            # Save image
            content = ContentFile(response.content, name=filename)
            product.image.save(filename, content, save=True)
            
            return True

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'    Error downloading from {url}: {e}')
            )
            return False
