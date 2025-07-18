"""
Express Deals - Load Service
High-performance bulk loading with multiple storage backends
"""

import asyncio
import logging
from typing import List, Dict, Optional
from datetime import datetime
from django.db import transaction
from django.core.cache import cache
from products.models import Product, Category
from scraping.models import ScrapedProduct, ScrapeJob

logger = logging.getLogger(__name__)


class HighPerformanceLoader:
    """Optimized bulk loading with error handling and validation"""
    
    def __init__(self):
        self.batch_size = 100
        self.retry_attempts = 3
        self.load_stats = {'loaded': 0, 'failed': 0, 'duplicates': 0}
    
    async def bulk_load_products(self, products_data: List[Dict], job_id: int) -> Dict:
        """Bulk load validated product data"""
        
        try:
            # Group by categories for efficient processing
            categorized_data = self._group_by_category(products_data)
            
            # Process in batches
            total_loaded = 0
            total_failed = 0
            
            for category_name, products in categorized_data.items():
                batch_result = await self._load_category_batch(
                    products, category_name, job_id
                )
                total_loaded += batch_result['loaded']
                total_failed += batch_result['failed']
            
            # Update job statistics
            await self._update_job_stats(job_id, total_loaded, total_failed)
            
            return {
                'success': True,
                'total_processed': len(products_data),
                'loaded': total_loaded,
                'failed': total_failed,
                'load_time': datetime.now()
            }
            
        except Exception as e:
            logger.error(f"Bulk load failed: {e}")
            return {
                'success': False,
                'error': str(e),
                'loaded': 0,
                'failed': len(products_data)
            }
    
    def _group_by_category(self, products_data: List[Dict]) -> Dict[str, List[Dict]]:
        """Group products by category for efficient processing"""
        categorized = {}
        
        for product in products_data:
            category = product.get('category', 'Other')
            if category not in categorized:
                categorized[category] = []
            categorized[category].append(product)
        
        return categorized
    
    async def _load_category_batch(self, products: List[Dict], category_name: str, job_id: int) -> Dict:
        """Load a batch of products for a specific category"""
        
        loaded_count = 0
        failed_count = 0
        
        try:
            # Get or create category
            category, created = await self._get_or_create_category(category_name)
            
            # Process products in smaller batches
            for i in range(0, len(products), self.batch_size):
                batch = products[i:i + self.batch_size]
                
                batch_result = await self._process_product_batch(
                    batch, category, job_id
                )
                
                loaded_count += batch_result['loaded']
                failed_count += batch_result['failed']
        
        except Exception as e:
            logger.error(f"Category batch load failed for {category_name}: {e}")
            failed_count = len(products)
        
        return {'loaded': loaded_count, 'failed': failed_count}
    
    async def _get_or_create_category(self, category_name: str) -> tuple:
        """Get or create category with caching"""
        cache_key = f'category_{category_name}'
        cached_category = cache.get(cache_key)
        
        if cached_category:
            return cached_category, False
        
        try:
            category, created = Category.objects.get_or_create(
                name=category_name,
                defaults={'description': f'Products in {category_name} category'}
            )
            
            # Cache for 1 hour
            cache.set(cache_key, category, timeout=3600)
            
            return category, created
            
        except Exception as e:
            logger.error(f"Failed to get/create category {category_name}: {e}")
            # Fallback to default category
            default_category, _ = Category.objects.get_or_create(
                name='Other',
                defaults={'description': 'Miscellaneous products'}
            )
            return default_category, False
    
    async def _process_product_batch(self, batch: List[Dict], category, job_id: int) -> Dict:
        """Process a batch of products with transaction safety"""
        
        loaded_count = 0
        failed_count = 0
        
        try:
            with transaction.atomic():
                for product_data in batch:
                    try:
                        # Create or update product
                        success = await self._create_or_update_product(
                            product_data, category, job_id
                        )
                        
                        if success:
                            loaded_count += 1
                        else:
                            failed_count += 1
                            
                    except Exception as e:
                        logger.error(f"Failed to process product: {e}")
                        failed_count += 1
                        
        except Exception as e:
            logger.error(f"Batch transaction failed: {e}")
            failed_count = len(batch)
        
        return {'loaded': loaded_count, 'failed': failed_count}
    
    async def _create_or_update_product(self, data: Dict, category, job_id: int) -> bool:
        """Create or update individual product"""
        
        try:
            # Extract required fields
            title = data.get('title', '').strip()
            price = data.get('price')
            source_url = data.get('source_url', '')
            
            if not title or not price or not source_url:
                logger.warning(f"Missing required fields: {data}")
                return False
            
            # Check for existing product by URL or title
            existing_product = None
            try:
                existing_product = Product.objects.filter(
                    source_url=source_url
                ).first()
                
                if not existing_product:
                    # Try to find by similar title
                    existing_product = Product.objects.filter(
                        title__iexact=title,
                        category=category
                    ).first()
                    
            except Exception as e:
                logger.debug(f"Error checking existing product: {e}")
            
            # Prepare product data
            product_data = {
                'title': title,
                'description': data.get('description', '')[:1000],  # Limit description
                'price': float(price),
                'category': category,
                'availability': data.get('availability', 'unknown'),
                'brand': data.get('brand', ''),
                'source_url': source_url,
                'image_url': self._get_primary_image(data.get('images', [])),
                'is_active': True,
                'updated_at': datetime.now()
            }
            
            if existing_product:
                # Update existing product
                for field, value in product_data.items():
                    if field != 'category':  # Don't overwrite category
                        setattr(existing_product, field, value)
                existing_product.save()
                product = existing_product
            else:
                # Create new product
                product = Product.objects.create(**product_data)
            
            # Create scraped product record
            await self._create_scraped_product_record(data, product, job_id)
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to create/update product: {e}")
            return False
    
    def _get_primary_image(self, images: List[str]) -> str:
        """Get the primary image URL from list"""
        if not images:
            return ''
        
        # Return first valid image
        for img in images:
            if img and isinstance(img, str) and img.startswith(('http://', 'https://')):
                return img
        
        return ''
    
    async def _create_scraped_product_record(self, data: Dict, product, job_id: int):
        """Create record in scraped products table"""
        
        try:
            ScrapedProduct.objects.create(
                job_id=job_id,
                product=product,
                external_id=data.get('external_id', ''),
                raw_data=data,
                quality_score=data.get('quality_score', 0.0),
                scraped_at=data.get('scraped_at', datetime.now())
            )
        except Exception as e:
            logger.warning(f"Failed to create scraped product record: {e}")
    
    async def _update_job_stats(self, job_id: int, loaded: int, failed: int):
        """Update scrape job statistics"""
        
        try:
            job = ScrapeJob.objects.get(id=job_id)
            job.products_imported = loaded
            job.errors_count = failed
            job.save()
        except Exception as e:
            logger.error(f"Failed to update job stats: {e}")
    
    def get_load_statistics(self) -> Dict:
        """Get loading performance statistics"""
        return {
            'loaded': self.load_stats['loaded'],
            'failed': self.load_stats['failed'],
            'duplicates': self.load_stats['duplicates'],
            'success_rate': (
                self.load_stats['loaded'] / 
                (self.load_stats['loaded'] + self.load_stats['failed'])
                if (self.load_stats['loaded'] + self.load_stats['failed']) > 0 
                else 0.0
            )
        }


# Global loader instance
loader = HighPerformanceLoader()
